from __future__ import annotations

from typing import Union

import jijmodeling_schema as pb

from ulid import ULID


def add_header_to_message(message: Union[pb.Expression, pb.Problem]) -> pb.Header:
    """
    Add header meta data to the `Expression` type message.

    Args:
        message (jijmodeling_schema.Expression): an `Expression` message

    Returns:
        jijmodeling_schema.Header: a `Header` message
    """
    # Create an empty `Header` message.
    header = pb.Header()

    # Make the id of the `Header` message.
    header.id = str(ULID())

    # Set the version of the JijModeling schema.
    header.version = "0.10.0"

    # Set the target message to the `header.value`.
    if type(message) is pb.Problem:
        header.value.problem = message
    elif type(message) is pb.Expression:
        header.value.expression = message

    return header
