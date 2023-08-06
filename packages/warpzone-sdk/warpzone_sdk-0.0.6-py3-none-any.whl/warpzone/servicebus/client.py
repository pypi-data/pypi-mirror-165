import typing
from functools import reduce

from azure.servicebus import (
    ServiceBusClient,
    ServiceBusMessage,
    ServiceBusReceiver,
    ServiceBusSender,
)


class WarpzoneSubscriptionClient:
    """Class to interact with Azure Service Bus Topic Subscription"""

    def __init__(self, subscription_receiver: ServiceBusReceiver):
        self._subscription_receiver = subscription_receiver

    @classmethod
    def from_connection_string(
        cls, conn_str: str, topic_name: str, subscription_name: str
    ):
        service_bus_client = ServiceBusClient.from_connection_string(conn_str)
        subscription_receiver = service_bus_client.get_subscription_receiver(
            topic_name, subscription_name
        )
        return cls(subscription_receiver)

    def receive_files(self) -> typing.Iterator[typing.Union[str, bytes]]:
        """Receive files from the service bus topic subscription."""
        with self._subscription_receiver:
            for msg in self._subscription_receiver:
                msg_data = msg.message.get_data()
                # message data can either be a generator
                # of string or bytes. We want to concatenate
                # them in either case
                content = reduce(lambda x, y: x + y, msg_data)
                yield content

    def get_latest_file(self, max_wait_time: int = 5) -> typing.Union[str, bytes]:
        """Get latest file from a service bus topic subscription.

        Args:
            max_wait_time (int): The time waiting for messages
        """
        self._subscription_receiver._max_wait_time = max_wait_time
        for content in self.receive_files():
            pass
        return content


class WarpzoneTopicClient:
    """Class to interact with Azure Service Bus Topic"""

    @classmethod
    def from_connection_string(cls, conn_str: str, topic_name: str):
        service_bus_client = ServiceBusClient.from_connection_string(conn_str)
        topic_sender = service_bus_client.get_topic_sender(topic_name)
        return WarpzoneTopicClient(topic_sender)

    def __init__(self, topic_sender: ServiceBusSender):
        self._topic_sender = topic_sender

    def send_file(self, content: str, subject: str, user_properties: dict = {}):
        """Send a file to the service bus topic.

        Args:
            content (str): The content of the message.
            subject (str): The subject of the message.
            user_properties (dict, optional): Custom user properties. Defaults to {}.
        """
        msg = ServiceBusMessage(
            content, subject=subject, application_properties=user_properties
        )

        with self._topic_sender:
            self._topic_sender.send_messages(msg)
