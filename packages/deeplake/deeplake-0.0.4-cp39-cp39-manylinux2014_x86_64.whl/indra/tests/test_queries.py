from indra import api
from .constants import COCO_DS_NAME, MNIST_DS_NAME, IMAGENET_DS_NAME, LAION_400_M_DS_NAME

from time import time

queries = {
    COCO_DS_NAME: [
        ("SELECT * WHERE categories[0] == 'person'", 22497),
        ("SELECT * WHERE shape(boxes)[0] == 5", 7712),
    ],
    MNIST_DS_NAME: [
        ("SELECT * WHERE labels == 0", 5923),
        ("SELECT * WHERE SHAPE(images)[0] == 28", 60000),
        ("SELECT * WHERE SHAPE(images)[0] == 29", 0),
    ],
    IMAGENET_DS_NAME: [
        ("SELECT * WHERE labels == 'bikini'", 1300),
        ("SELECT * WHERE SHAPE(boxes)[0] > 15", 2),
        ("(SELECT * WHERE labels == 'bikini' LIMIT 10) UNION (SELECT * WHERE labels == 1 LIMIT 10) UNION (SELECT * WHERE labels == 43 LIMIT 10)", 30),
    ],
    LAION_400_M_DS_NAME: [
        ("SELECT * WHERE CONTAINS(caption, 'blue')", 2783),
        ("SELECT * WHERE caption[0] == 'A'", 28904),
        ("SELECT * WHERE SHAPE(image)[0] == 256", 512993),
    ],
}

def test_dataset_query_resutls():
    global queries
    for ds_name in queries:
        ds = api.dataset(ds_name)
        for (query, result_size) in queries[ds_name]:
            print(f"\tRunning query: {query}")
            start = time()
            result = ds.query(query)
            print('\tQuery time: ', time() - start)
            assert(len(result) == result_size)