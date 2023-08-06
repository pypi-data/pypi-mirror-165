""" Module w.r.t. Azure table storage logic."""

import os
import typing

from azure.data.tables import TableClient, TableServiceClient

from .operations import TableOperations


class WarpzoneTableClient:
    """Class to interact with Azure Table Storage."""

    def __init__(self, table_name: str):
        self.table_name = table_name
        self._service: TableServiceClient = self._get_table_service()
        self._table: TableClient = self._get_table_client()

    def _get_table_service(self) -> TableServiceClient:
        """Get table service."""
        conn_string = os.environ["WARPZONE_DATA_CONNECTION_STRING"]

        return TableServiceClient.from_connection_string(conn_string)

    def _get_table_client(self) -> TableClient:
        """Get table client from service connection"""
        return self._service.get_table_client(self.table_name)

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
            self._table.submit_transaction(chunk)

    def query(self, query: str) -> typing.List[typing.Dict]:
        """Retrieve data from Table Storage using linq query

        Args:
            query (str): Linq query.

        Returns:
            typing.List[typing.Dict]: List of entities.
        """
        entities = [record for record in self._table.query_entities(query)]

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
