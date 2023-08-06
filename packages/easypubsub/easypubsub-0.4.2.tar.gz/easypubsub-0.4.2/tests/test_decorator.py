import time

from easypubsub.decorator import publish_this
from easypubsub.proxy import Proxy
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

    @publish_this(name="test_publisher", topic="test_topic", address=PUBLISHERS_ADDRESS)
    def publish_a_message(extra: str):
        return f"This the {extra} message"

    publish_a_message("first")

    # Create a Subscriber.
    subscriber = Subscriber(
        "test_subscriber", SUBSCRIBERS_ADDRESS, topics="test_publisher.test_topic"
    )

    # Wait for connection to establish.
    time.sleep(1.0)
    publish_a_message("second")
    messages = subscriber.receive()
    time.sleep(1.0)  # Give some time for the messages to be received.
    assert len(messages) == 1
    assert messages[0] == ("test_publisher.test_topic", "This the second message")

    publish_a_message("new first")
    messages = subscriber.receive()
    time.sleep(1.0)  # Give some time for the messages to be received.
    assert messages[0] == ("test_publisher.test_topic", "This the new first message")
    # Stop the Proxy.
    proxy.stop()
