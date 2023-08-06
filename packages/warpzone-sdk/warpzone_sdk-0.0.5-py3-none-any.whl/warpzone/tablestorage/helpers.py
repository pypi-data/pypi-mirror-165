import typing


def chunkify(lst: typing.List, max_chunk_size: int) -> typing.List[typing.List]:
    """Split list into n lists that does not exceed max_chunk_size.

    Args:
        lst (typing.List): Initial list of things.
        max_chunk_size (int): The maximum size of the chunks.

    Returns:
        typing.List[typing.List]: List of lists.
    """
    if max_chunk_size <= 0:
        raise ValueError("max_chunk_size must be greater than 0.")

    if not lst:
        return []

    n = len(lst) // max_chunk_size + 1

    return [lst[i::n] for i in range(n)]
