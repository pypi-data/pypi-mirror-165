import pickle

import pytest

from easypubsub.publisher import Publisher

PUBLISHERS_ADDRESS = "tcp://127.0.0.1:5555"
PICKLING_ERROR_STRING = "Can't pickle local object"


def test_unpicklability():
    # This is to test that the lambda is not picklable.
    with pytest.raises(AttributeError, match=PICKLING_ERROR_STRING):
        pickle.dumps(lambda x: 2 * x)


def test_publish_unpicklability():
    publisher = Publisher(
        "test_publisher", PUBLISHERS_ADDRESS, default_topic="test_topic"
    )
    publisher.publish("This is a first test message.")

    with pytest.raises(AttributeError, match=PICKLING_ERROR_STRING):
        publisher.publish(lambda x: 2 * x)
