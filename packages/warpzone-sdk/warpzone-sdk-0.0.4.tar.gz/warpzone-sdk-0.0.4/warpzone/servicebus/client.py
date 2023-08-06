import os

from azure.servicebus import ServiceBusClient, ServiceBusMessage


class WarpzoneBusClient:
    def __init__(self, topic: str):
        self.topic = topic
        self._client = self._get_servicebus_client()

    def _get_servicebus_client(self) -> ServiceBusClient:
        """Get table client from service connection"""
        conn_string = os.environ["SERVICEBUS_CONNECTION_STRING"]

        return ServiceBusClient.from_connection_string(conn_string)

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

        with self._client:
            sender = self._client.get_topic_sender(topic_name=self.topic)
            with sender:
                sender.send_messages(msg)
