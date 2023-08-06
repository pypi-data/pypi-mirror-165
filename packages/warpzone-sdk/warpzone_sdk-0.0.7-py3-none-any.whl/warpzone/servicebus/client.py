from functools import reduce
from typing import Iterator, Union

from azure.servicebus import ServiceBusClient, ServiceBusMessage


class WarpzoneSubscriptionClient:
    """Class to interact with Azure Service Bus Topic Subscription"""

    def __init__(
        self,
        service_bus_client: ServiceBusClient,
        topic_name: str,
        subscription_name: str,
    ):
        self._service_bus_client = service_bus_client
        self.topic_name = topic_name
        self.subscription_name = subscription_name

    @classmethod
    def from_connection_string(
        cls, conn_str: str, topic_name: str, subscription_name: str
    ) -> "WarpzoneSubscriptionClient":
        service_bus_client = ServiceBusClient.from_connection_string(conn_str)
        return cls(service_bus_client, topic_name, subscription_name)

    def _get_subscription_receiver(self, max_wait_time: int = None):
        return self._service_bus_client.get_subscription_receiver(
            self.topic_name, self.subscription_name, max_wait_time=max_wait_time
        )

    def receive_files(self, max_wait_time: int = None) -> Iterator[Union[str, bytes]]:
        """Receive files from the service bus topic subscription."""
        with self._get_subscription_receiver(max_wait_time) as receiver:
            for msg in receiver:
                msg_data = msg.message.get_data()
                # message data can either be a generator
                # of string or bytes. We want to concatenate
                # them in either case
                content = reduce(lambda x, y: x + y, msg_data)
                yield content

    def get_latest_file(self, max_wait_time: int = 5) -> Union[str, bytes]:
        """Get latest file from a service bus topic subscription.

        Args:
            max_wait_time (int): The time waiting for messages

        Returns:
            Union[str, bytes]: The latest file from the subscription
        """
        content = None
        for content in self.receive_files(max_wait_time):
            pass

        return content


class WarpzoneTopicClient:
    """Class to interact with Azure Service Bus Topic"""

    def __init__(self, service_bus_client: ServiceBusClient, topic_name: str):
        self._service_bus_client = service_bus_client
        self.topic_name = topic_name

    @classmethod
    def from_connection_string(
        cls, conn_str: str, topic_name: str
    ) -> "WarpzoneTopicClient":
        service_bus_client = ServiceBusClient.from_connection_string(conn_str)
        return WarpzoneTopicClient(service_bus_client, topic_name)

    def _get_topic_sender(self):
        return self._service_bus_client.get_topic_sender(self.topic_name)

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

        with self._get_topic_sender() as sender:
            sender.send_messages(msg)
