from easypubsub.publisher import Publisher


class publish_this:
    """
    Decorator for publishing values returned by functions.
    See :obj:`~easypubsub.publisher.Publisher` for more information about the arguments.

    Example:
        >>> @publish_this(name="lottery", topic="winning_number", address="tcp://localhost:5555")
        >>> def my_random_number_generator():
        >>>     return random.randint(1, 100)
        ...
        >>> my_random_number_generator()  # This just got published to the topic "lottery.winning_number"
    """

    def __init__(self, name: str, topic: str, address: str):
        self.name = name
        self.topic = topic
        self.address = address

        self.publisher = Publisher(name, address, topic)

    def __call__(self, func):
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            self.publisher.publish(result)
            return result

        return wrapper
