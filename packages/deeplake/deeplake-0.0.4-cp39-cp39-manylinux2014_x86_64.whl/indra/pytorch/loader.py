from itertools import repeat
from typing import Callable, List, Optional
from indra.pytorch.util import get_indexes, transform_collate_batch
from indra.pytorch.common import collate_fn as default_collate
import multiprocessing as mp
from pathos.pools import ProcessPool

try:
    import torch
    torch.set_num_threads(1)
except ImportError:
    pass

class Loader:
    def __init__(
        self,
        dataset,
        batch_size: Optional[int] = 1,
        shuffle: bool = False,
        drop_last: bool = False,
        transform_fn: Optional[Callable] = None,
        num_workers: int = 0,
        num_threads: Optional[int] = None,
        collate_fn: Optional[Callable] = default_collate,
        distributed=False,
        tensors: Optional[List[str]] = None,
        prefetch_factor: int = 10,
        upcast: bool = True,
    ):
        if num_workers < 0:
            raise ValueError("num_workers must be non-negative")
        if num_threads is not None and num_threads <= 0:
            raise ValueError("num_threads must be positive")
        tensors = tensors or []
        self.dataset = dataset
        self.batch_size = batch_size
        self.shuffle = shuffle
        self.drop_last = drop_last
        self.transform_fn = transform_fn
        self.num_workers = num_workers
        self.num_threads = num_threads
        self.collate_fn = collate_fn
        self.distributed = distributed
        self.tensors = tensors
        self.prefetch_factor = prefetch_factor
        self.upcast = upcast
        self.pool = None
        self.dataloader = None

    def start_processes(self):
        if self.pool is not None:
            return
        self.pool = ProcessPool(nodes=self.num_workers)
        m = mp.Manager()
        self.data_in_queues = [m.Queue() for _ in range(self.num_workers)]
        self.data_out_queues = [m.Queue() for _ in range(self.num_workers)]

    def run_workers(self):
        inp = list(zip(self.data_in_queues, self.data_out_queues, repeat(self.transform_fn), repeat(self.collate_fn), repeat(self.upcast)))
        self.pool.amap(early_transform_collate, inp)

    def __iter__(self):
        if self.dataloader is None:
            dataset = self.dataset
            if self.distributed:
                indexes = get_indexes(dataset, shuffle=self.shuffle)
                dataset = dataset[indexes]
        
            self.dataloader = create_dataloader(
                dataset = dataset, drop_last=self.drop_last, batch_size=self.batch_size, num_threads=self.num_threads, tensors=self.tensors, shuffle=self.shuffle
            )
        
        if self.num_workers == 0:
            yield from self.zero_worker_iter()
        else:
            yield from self.multiprocess_iter()

    def zero_worker_iter(self):
        for batch in self.dataloader:
            out = transform_collate_batch(batch, self.transform_fn, self.collate_fn, self.upcast)
            yield out

    def multiprocess_iter(self):
        self.start_processes()
        self.run_workers()
        num_prefetch_tasks = self.prefetch_factor * self.num_workers
        dataloader = self.dataloader
        i = 0
        while 1:
            wid = i % self.num_workers
            if i >= num_prefetch_tasks:
                out = self.data_out_queues[wid].get()
                if out is None:
                    # get None from other workers too, to empty the queues
                    for j in range(self.num_workers):
                        if j != wid:
                            self.data_out_queues[j].get()
                    break
                if isinstance(out, Exception):
                    raise out

            if i < len(dataloader):
                batch = next(dataloader)
                self.data_in_queues[wid].put(batch)
            elif i == len(dataloader):
                try:
                    next(dataloader)
                except StopIteration:
                    pass
                # send None (stop signal) to all workers
                for j in range(self.num_workers):
                    self.data_in_queues[j].put(None)
            if i >= num_prefetch_tasks:
                yield out
            i += 1


def create_dataloader(
    dataset, batch_size, num_threads, tensors, drop_last=False, shuffle=False
):
    if num_threads is None:
        return dataset.loader(
            batch_size=batch_size,
            tensors=tensors,
            drop_last=drop_last,
            shuffle=shuffle,
        )

    return dataset.loader(
        batch_size=batch_size,
        num_threads=num_threads,
        tensors=tensors,
        drop_last=drop_last,
        shuffle=shuffle,
    )


def early_transform_collate(inp):
    data_in_queue, data_out_queue, transform_fn, collate_fn, upcast = inp
    while(1):
        batch = data_in_queue.get()
        if batch is None:
            data_out_queue.put(None)
            break
        try:
            out = transform_collate_batch(batch, transform_fn, collate_fn, upcast)
            data_out_queue.put(out)
        except Exception as e:
            data_out_queue.put(e)
            break
