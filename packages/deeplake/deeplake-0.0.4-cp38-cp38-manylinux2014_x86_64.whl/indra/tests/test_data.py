from indra import api, Loader
from .constants import MNIST_DS_NAME, COCO_DS_NAME
import numpy as np
import hub
import pickle
import shutil
from  hub.util.exceptions import TokenPermissionError

CHECKOUT_TEST_DIRECTORY = "./data/checkout_directory"

def test_coco_bmasks_equality():
    """
    check binary masks consitency for coco_train dataset
    """
    cpp_ds = api.dataset(COCO_DS_NAME)[0:100]
    hub_ds = hub.load(COCO_DS_NAME)[0:100]

    assert len(cpp_ds) == len(hub_ds)
    assert cpp_ds.tensors[2].name == "masks"
    assert cpp_ds.tensors[0].name == "images"
    for i in range(100):
        assert np.array_equal(hub_ds.masks[i].numpy(), cpp_ds.tensors[2][i])
        assert hub_ds.images[i].numpy().shape == cpp_ds.tensors[0][i].shape


def test_mnist_images_equality():
    cpp_ds = api.dataset(MNIST_DS_NAME)[0:100]
    hub_ds = hub.load(MNIST_DS_NAME)[0:100]

    assert len(cpp_ds) == len(hub_ds)
    assert cpp_ds.tensors[0].name == "images"
    for i in range(100):
        assert np.array_equal(hub_ds.images[i].numpy(), cpp_ds.tensors[0][i])

    assert cpp_ds.tensors[1].name == "labels"
    for i in range(100):
        assert np.array_equal(hub_ds.images[i].numpy(), cpp_ds.tensors[0][i])


def iter_on_loader():
    ds = api.dataset(MNIST_DS_NAME)[0:100]
    dl = Loader(
        ds,
        batch_size=2,
        transform_fn=lambda x: x,
        num_threads=4,
        tensors = [],
    )

    for i, batch in enumerate(dl):
        print(f"hub3 : {batch['labels']}")
        break


def test_dataloader_destruction():
    """
    create dataloader on a separate function multiple times check if the dataloader and dataset destruction is done normally
    """
    for i in range(4):
        iter_on_loader()


def test_s3_dataset_pickling():
    ds = api.dataset("s3://hub-2.0-datasets-n/cars/")
    before = len(ds)
    pickled_ds = pickle.dumps(ds)
    new_ds = pickle.loads(pickled_ds)
    after = len(new_ds)
    assert after == before
    assert new_ds.path == ds.path


def test_s3_sliced_dataset_pickling():
    ds = api.dataset("s3://hub-2.0-datasets-n/cars/")[0:1000]
    ds = ds[1:100]
    pickled_ds = pickle.dumps(ds)
    new_ds = pickle.loads(pickled_ds)
    assert len(new_ds) == len(ds)
    assert new_ds.path == ds.path

    ds = new_ds[[0, 12, 14, 15, 30, 50, 60, 70, 71, 72, 72, 76]]
    before = len(ds)
    pickled_ds = pickle.dumps(ds)
    unpickled_ds = pickle.loads(pickled_ds)
    assert len(unpickled_ds) == len(ds) == 12


def test_hub_sliced_dataset_pickling():
    ds = api.dataset(MNIST_DS_NAME)[0:1000]
    ds = ds[1:100]
    pickled_ds = pickle.dumps(ds)
    new_ds = pickle.loads(pickled_ds)
    assert len(new_ds) == len(ds)
    assert new_ds.path == ds.path

    ds = new_ds[[0, 12, 14, 15, 30, 50, 60, 70, 71, 72, 72, 76]]
    pickled_ds = pickle.dumps(ds)
    unpickled_ds = pickle.loads(pickled_ds)
    assert len(unpickled_ds) == len(ds) == 12


def test_pickleing():
    ds = api.dataset(MNIST_DS_NAME)
    l_ds = ds[[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]]
    pickled_ds = pickle.dumps(l_ds)
    another = pickle.loads(pickled_ds)
    assert len(another) == 10

    s_ds = ds[1:1000]
    pickled_ds = pickle.dumps(s_ds)
    another = pickle.loads(pickled_ds)
    assert len(another) == 999

    s_ds = s_ds[10:300]
    pickled_ds = pickle.dumps(s_ds)
    another = pickle.loads(pickled_ds)
    assert len(another) == 290

    s_ds = s_ds[10:30]
    pickled_ds = pickle.dumps(s_ds)
    another = pickle.loads(pickled_ds)
    assert len(another) == 20

def test_if_dataset_exists():
    try:
        ds = api.dataset("s3://some_ordinary/bucket")
    except RuntimeError as e:
        print(e)
        assert str(e) == "Specified dataset does not exists"

    try:
        ds = api.dataset("hub://activeloop/cars_a")
    except TokenPermissionError:
        pass

def test_dataset_slicing():
    ds = api.dataset(MNIST_DS_NAME)[0:100]
    assert(len(ds) == 100)

    try:
        ds1 = ds[[0, 7, 10, 6, 7]]
        assert(len(ds1) == 5)
        ds2 = ds1[[7]]
    except IndexError:
        pass

def test_wrong_checkout():
    ds = api.dataset(MNIST_DS_NAME)[0:100]
    assert(len(ds) == 100)

    try:
        ds.checkout("some_hash")
    except RuntimeError as e:
        assert str(e) == "Provided commit_id \"some_hash\" does not exist"

    ds.checkout("firstdbf9474d461a19e9333c2fd19b46115348f")


def test_checkout_with_ongoing_hash():
    try:
        shutil.rmtree(CHECKOUT_TEST_DIRECTORY)
    except FileNotFoundError:
        pass
    ds = hub.dataset(CHECKOUT_TEST_DIRECTORY, overwrite=True)
    with ds:
        ds.create_tensor("image")
        ds.image.extend(([i * np.ones((i + 1, i + 1)) for i in range(16)]))
        ds.commit()
        ds.create_tensor("image2")
        ds.image2.extend(np.array([i * np.ones((12, 12)) for i in range(16)]))

    commit_id = ds.pending_commit_id
    ds2 = api.dataset(CHECKOUT_TEST_DIRECTORY)
    ds2.checkout(commit_id)
