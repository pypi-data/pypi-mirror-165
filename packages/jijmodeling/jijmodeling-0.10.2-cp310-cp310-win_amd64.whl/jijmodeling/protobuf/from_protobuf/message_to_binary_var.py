from typing import List

import jijmodeling_schema as pb

from jijmodeling.expression.variables.deci_vars import Binary


def message_to_binary_var(
    id: str, message: pb.BinaryVar, shape: List[pb.Expression]
) -> Binary:
    """
    Convert a message to a `Binary` object.

    Args:
        id (str): the id of the `Binary` object
        message (pb.BinaryVar): the `BinaryVar` message
        shape (List[pb.Expression]): the shape of the `Binary` object

    Raises:
        ValueError: the error occurs if `dim` is not equal to length of the shape

    Returns:
        Binary: a `Binary` object
    """
    # Validate length of the shape.
    if message.dim != len(shape):
        raise ValueError("invalid length of the shape")

    # Set the symbol.
    symbol = message.symbol

    # NOTE: Import a module within a local scope to fix a circular import.
    # - https://stackoverflow.com/questions/59462679/design-of-python-conditional-imports
    # - https://medium.com/@hamana.hadrien/so-you-got-a-circular-import-in-python-e9142fe10591
    from jijmodeling.protobuf.from_protobuf.message_to_expression import (
        message_to_expression,
    )

    # Set the shape.
    shape_element_list = [
        message_to_expression(shape_element) for shape_element in shape
    ]

    return Binary(label=symbol, shape=shape_element_list, uuid=id)
