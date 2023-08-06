""" Module w.r.t. data transformation."""

import base64 as b64

import pandas as pd
import pyarrow as pa


def msg_to_pandas_dataframe(message_body: bytes) -> pd.DataFrame:
    """This function takes a Azure servicebus message transform it into a
    pandas dataframe.

    Args:
        message (bytes): The body of a Azure Service Bus message in bytes.
        encoding (str, optional): Encoding of the message. Defaults to "utf-8".

    Returns:
        pd.DataFrame: A pandas dataframe with the decoded data.
    """
    parquet_file = b64.b64decode(message_body)
    buf = pa.py_buffer(parquet_file)

    return pd.read_parquet(buf)


def pandas_dataframe_to_msg(df: pd.DataFrame) -> bytes:
    """This function takes a pandas dataframe transform it into a
    Azure servicebus message.

    Args:
        df (pd.DataFrame): A pandas dataframe
        encoding (str, optional): Encoding of the message. Defaults to "utf-8".

    Returns:
        bytes: The body of a Azure Service Bus message in bytes.
    """
    buf = pa.BufferOutputStream()
    df.to_parquet(buf)
    parquet_file = buf.getvalue().to_pybytes()
    message_body = b64.b64encode(parquet_file)

    return message_body
