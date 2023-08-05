from indra import api, Loader
from .constants import MNIST_DS_NAME, CIFAR10_DS_NAME
import torch
import hub
import numpy as np
from indra.pytorch.helper_fns import transform_fn
from torchvision import transforms


TFORM = transforms.Compose(
    [
        transforms.ToPILImage(),  # Must convert to PIL image for subsequent operations to run
        transforms.RandomRotation(20),  # Image augmentation
        transforms.ToTensor(),  # Must convert to pytorch tensor for subsequent operations to run
        transforms.Normalize([0.5, 0.5, 0.5], [0.5, 0.5, 0.5]),
    ]
)


def _cpp_transform(sample):
    sample["images"] = TFORM(sample["images"])
    return sample


def test_on_with_s3_path_loader():
    cpp_ds = api.dataset("s3://hub-2.0-datasets-n/cars/")[0:100]
    hub_ds = hub.load("s3://hub-2.0-datasets-n/cars/")[0:100]

    for i in range(100):
        np.testing.assert_array_equal(hub_ds.images[i].numpy(), cpp_ds.tensors[0][i])


def test_mnist_batch_equality():
    cpp_ds = api.dataset(MNIST_DS_NAME)[0:100]
    hub_ds = hub.load(MNIST_DS_NAME)[0:100]

    def transform_fn(item):
        return item

    cpp_iter = iter(
        Loader(
            cpp_ds,
            batch_size=1,
            transform_fn=transform_fn,
            num_threads=1,
        )
    )

    hub_iter = iter(hub_ds.pytorch(transform=transform_fn, batch_size=1))

    for _ in range(10):
        a = next(cpp_iter)
        b = next(hub_iter)
        torch.equal(a["images"], b["images"])
        torch.equal(a["labels"], b["labels"])



def test_cifar10_batch_equality():
    cpp_ds = api.dataset(CIFAR10_DS_NAME)[0:100]
    hub_ds = hub.load(CIFAR10_DS_NAME)[0:100]

    cpp_iter = iter(
        Loader(
            cpp_ds,
            batch_size=1,
            transform_fn=_cpp_transform,
            num_threads=1,
            tensors = [],
        )
    )

    hub_iter = iter(
        hub_ds.pytorch(transform={"images": TFORM, "labels": None}, batch_size=1)
    )

    for i in range(10):
        torch.equal(next(cpp_iter)["images"], next(hub_iter)["images"])


def test_cifar10_batch_with_multiple_workersequality():
    cpp_ds = api.dataset(CIFAR10_DS_NAME)[0:100]
    hub_ds = hub.load(CIFAR10_DS_NAME)[0:100]

    cpp_iter = iter(
        Loader(
            cpp_ds,
            batch_size=1,
            transform_fn=_cpp_transform,
            num_threads=2,
            tensors = [],
        )
    )

    hub_iter = iter(
        hub_ds.pytorch(
            num_workers=2, transform={"images": TFORM, "labels": None}, batch_size=1
        )
    )

    for i in range(10):
        torch.equal(next(cpp_iter)["images"], next(hub_iter)["images"])


def test_data_loader_tensor_extraction():
    ds = api.dataset(MNIST_DS_NAME)[0:10]
    def collate_fn(batch):
        return batch

    try:
        ld = ds.loader(tensors=["aa"])
    except KeyError:
        pass

    it = iter(ds.loader(tensors=["images"], batch_size=1))

    for item in it:
        assert len(item[0].keys()) == 1
        assert item[0].get("images", None) is not None

def test_data_loader_drop_last():
    ds = api.dataset(MNIST_DS_NAME)[0:10]

    ld1 = ds.loader(drop_last=True, batch_size=3)
    assert len(ld1) == 3

    ld2 = ds.loader(drop_last=False, batch_size=3)
    assert len(ld2) == 4