from typing import List

import jijmodeling_schema as pb

from jijmodeling.expression.variables.variable import Subscripts


def message_to_subscript_op(
    id: str, message: pb.SubscriptOp, children: List[pb.Expression]
) -> Subscripts:
    """
    Convert a message to a `Subscripts` object.

    Args:
        id (str): the id of the `Subscripts` object.
        message (pb.SubscriptOp): the `SubscriptOp` message
        children (List[pb.Expression]): 0: the array, 1..: the subscripts of the `Subscripts` object

    Raises:
        ValueError: the error occurs if `num_subs` is not equal to length of the subscript

    Returns:
        Subscripts: a `Subscripts` object
    """
    # Validate length of the subscripts.
    if message.num_subs + 1 != len(children):
        raise ValueError(
            f"invalid length of the subscripts, expect = {message.num_subs} but actual = {len(children) - 1}"
        )

    # NOTE: Import a module within a local scope to fix a circular import.
    # - https://stackoverflow.com/questions/59462679/design-of-python-conditional-imports
    # - https://medium.com/@hamana.hadrien/so-you-got-a-circular-import-in-python-e9142fe10591
    from jijmodeling.protobuf.from_protobuf.message_to_expression import (
        message_to_expression,
    )

    # Set the array.
    array = message_to_expression(children[0])

    # Set the subscripts.
    subscripts = [message_to_expression(expr) for expr in children[1:]]

    return Subscripts(variable=array, subscripts=subscripts, uuid=id)
