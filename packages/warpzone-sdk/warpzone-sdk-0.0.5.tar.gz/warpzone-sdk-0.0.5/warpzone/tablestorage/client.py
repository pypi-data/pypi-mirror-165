""" Module w.r.t. Azure table storage logic."""

import typing

from azure.data.tables import TableClient

from .operations import TableOperations


class WarpzoneTableClient:
    """Class to interact with Azure Table"""

    def __init__(self, table_client: TableClient):
        self._table_client = table_client

    @classmethod
    def from_connection_string(cls, conn_str: str, table_name: str):
        table_client = TableClient.from_connection_string(conn_str, table_name)
        return cls(table_client)

    def execute_table_operations(
        self,
        operations: TableOperations,
    ):
        """Perform table storage operations from a operation set.

        Args:
            operations (typing.List[typing.List]): List of lists with operations for a
            given dataframe.
        """
        for chunk in operations:
            self._table_client.submit_transaction(chunk)

    def query(self, query: str) -> typing.List[typing.Dict]:
        """Retrieve data from Table Storage using linq query

        Args:
            query (str): Linq query.

        Returns:
            typing.List[typing.Dict]: List of entities.
        """
        entities = [record for record in self._table_client.query_entities(query)]

        return entities

    def query_partition(self, partition_key: str) -> typing.List[typing.Dict]:
        """Retrieve data from Table Storage using partition key

        Args:
            partition_key (str): Partion key.

        Returns:
            typing.List[typing.Dict]: List of entities.
        """
        query = f"PartitionKey eq '{partition_key}'"

        return self.query(query)
