import time

from easypubsub.proxy import Proxy
from easypubsub.publisher import Publisher
from easypubsub.subscriber import Subscriber

PUBLISHERS_ADDRESS = "tcp://127.0.0.1:5555"
SUBSCRIBERS_ADDRESS = "tcp://127.0.0.1:5556"


def test_simple_pubsub():
    """
    Test the simple Publish/Subscribe functionality.
    """

    # Create a Proxy.
    proxy = Proxy(PUBLISHERS_ADDRESS, SUBSCRIBERS_ADDRESS)
    proxy.launch()

    # Create a Publisher.
    publisher = Publisher(
        "test_publisher", PUBLISHERS_ADDRESS, default_topic="test_topic"
    )
    publisher.publish("This is a first test message.")

    # Create a Subscriber.
    subscriber = Subscriber(
        "test_subscriber", SUBSCRIBERS_ADDRESS, topics="test_publisher.test_topic"
    )

    # Wait for connection to establish.
    time.sleep(1.0)
    publisher.publish("This is a second test message.")
    messages = subscriber.receive()
    time.sleep(1.0)  # Give some time for the messages to be received.
    assert len(messages) == 1

    # Stop the Proxy.
    proxy.stop()


def test_final_dot_topic():
    # Create a Proxy.
    proxy = Proxy(PUBLISHERS_ADDRESS, SUBSCRIBERS_ADDRESS)
    proxy.launch()

    subscriber = Subscriber(
        "test_subscriber", SUBSCRIBERS_ADDRESS, topics="test_publisher.test_topic"
    )

    publisher = Publisher(
        "test_publisher", PUBLISHERS_ADDRESS, default_topic="test_topic."
    )
    time.sleep(1.0)

    publisher.publish(
        "This message should be delivered even if the topic ends with a dot."
    )
    messages = subscriber.receive()
    time.sleep(1.0)  # Give some time for the messages to be received.
    assert len(messages) == 1
    assert messages[0] == (
        "test_publisher.test_topic",
        "This message should be delivered even if the topic ends with a dot.",
    )
    proxy.stop()


def test_many_final_dots():
    proxy = Proxy(PUBLISHERS_ADDRESS, SUBSCRIBERS_ADDRESS)
    proxy.launch()

    subscriber = Subscriber(
        "test_subscriber", SUBSCRIBERS_ADDRESS, topics="test_publisher.test_topic"
    )

    publisher = Publisher(
        "test_publisher", PUBLISHERS_ADDRESS, default_topic="test_topic...."
    )
    time.sleep(1.0)

    publisher.publish(
        "This message should be delivered even if the topic ends with many dots."
    )
    messages = subscriber.receive()
    time.sleep(1.0)  # Give some time for the messages to be received.
    assert len(messages) == 1
    assert messages[0] == (
        "test_publisher.test_topic",
        "This message should be delivered even if the topic ends with many dots.",
    )
    proxy.stop()


def test_subscribe_to_all_topics():
    proxy = Proxy(PUBLISHERS_ADDRESS, SUBSCRIBERS_ADDRESS)
    proxy.launch()

    subscriber = Subscriber("test_subscriber", SUBSCRIBERS_ADDRESS)

    publisher_1 = Publisher(
        "test_publisher_1", PUBLISHERS_ADDRESS, default_topic="test_topic_1"
    )
    publisher_2 = Publisher(
        "test_publisher_2", PUBLISHERS_ADDRESS, default_topic="test_topic_2"
    )
    time.sleep(1.0)

    publisher_1.publish("This is a message.")
    publisher_2.publish("This is another message.")
    messages = subscriber.receive()
    time.sleep(1.0)  # Give some time for the messages to be received.
    assert len(messages) == 2
    proxy.stop()


def test_subscribe_to_some_topics():
    proxy = Proxy(PUBLISHERS_ADDRESS, SUBSCRIBERS_ADDRESS)
    proxy.launch()

    subscriber = Subscriber(
        "test_subscriber",
        SUBSCRIBERS_ADDRESS,
        topics=[
            "test_publisher_1",
            "test_publisher_4",
        ],
    )

    publisher_1 = Publisher(
        "test_publisher_1", PUBLISHERS_ADDRESS, default_topic="test_topic_1"
    )
    publisher_2 = Publisher(
        "test_publisher_2", PUBLISHERS_ADDRESS, default_topic="test_topic_2"
    )
    publisher_3 = Publisher(
        "test_publisher_3", PUBLISHERS_ADDRESS, default_topic="test_topic_3"
    )
    publisher_4 = Publisher(
        "test_publisher_4", PUBLISHERS_ADDRESS, default_topic="test_topic_4"
    )
    time.sleep(1.0)

    publisher_1.publish("This is a message.")
    publisher_2.publish("This is another message.")
    publisher_3.publish("This is a third message.")
    publisher_4.publish("This is a fourth message.")
    messages = subscriber.receive()
    time.sleep(1.0)  # Give some time for the messages to be received.
    assert len(messages) == 2
    proxy.stop()
