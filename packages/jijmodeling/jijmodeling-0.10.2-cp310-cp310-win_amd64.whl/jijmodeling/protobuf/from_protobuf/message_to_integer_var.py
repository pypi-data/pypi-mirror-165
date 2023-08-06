from typing import List

import jijmodeling_schema as pb

from jijmodeling.expression.variables.deci_vars import Integer


def message_to_integer_var(
    id: str, message: pb.IntegerVar, children: List[pb.Expression]
) -> Integer:
    """
    Convert a message to an `Integer` object.

    Args:
        id (str): the id of the `Integer` object
        message (pb.IntegerVar): the `IntegerVar` message
        children (List[pb.Expression]): 0: lower bound, 1: upper bound, 2..: the shape of the `Integer` object

    Raises:
        ValueError: the error occurs if `dim` is not equal to length of the shape

    Returns:
        Integer: an `Integer` object
    """
    # Validate length of the shape.
    if message.dim + 2 != len(children):
        raise ValueError("invalid length of the shape")

    # Set the symbol.
    symbol = message.symbol

    # NOTE: Import a module within a local scope to fix a circular import.
    # - https://stackoverflow.com/questions/59462679/design-of-python-conditional-imports
    # - https://medium.com/@hamana.hadrien/so-you-got-a-circular-import-in-python-e9142fe10591
    from jijmodeling.protobuf.from_protobuf.message_to_expression import (
        message_to_expression,
    )

    # Set the lower.
    lower = message_to_expression(children[0])

    # Set the upper.
    upper = message_to_expression(children[1])

    # Set the shape.
    shape_element_list = [
        message_to_expression(shape_element) for shape_element in children[2:]
    ]

    return Integer(
        label=symbol, lower=lower, upper=upper, shape=shape_element_list, uuid=id
    )
