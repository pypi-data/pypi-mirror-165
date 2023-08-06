from typing import List

import jijmodeling_schema as pb

from jijmodeling.expression.prod import ProdOperator
from jijmodeling.expression.sum import ReductionOperator, SumOperator


def message_to_reduction_op(
    id: str, message: pb.ReductionOp, children: List[pb.Expression]
) -> ReductionOperator:
    """
    Convert a message to a `ReductionOperator` object.

    Args:
        id (str): the id of the `ReductionOperator` object.
        message (pb.ReductionOp): the `ReductionOp` message
        children (List[pb.Expression]): 0: the index, 1: the operand, 2(optional): the condition expression

    Returns:
        ReductionOperator: a `ReductionOperator` object.
    """
    # NOTE: Import a module within a local scope to fix a circular import.
    # - https://stackoverflow.com/questions/59462679/design-of-python-conditional-imports
    # - https://medium.com/@hamana.hadrien/so-you-got-a-circular-import-in-python-e9142fe10591
    from jijmodeling.protobuf.from_protobuf.message_to_expression import (
        message_to_expression,
    )

    # Set the index.
    index = message_to_expression(children[0])

    # Set the operand.
    operand = message_to_expression(children[1])

    # Check if the message has a condition expression.
    if message.has_condition:
        # Set the condition expression.
        condition = message_to_expression(children[2])
    else:
        condition = None

    if message.kind == pb.ReductionOpKind.SUM:
        return SumOperator(
            sum_index=index, operand=operand, condition=condition, uuid=id
        )
    elif message.kind == pb.ReductionOpKind.PROD:
        return ProdOperator(
            sum_index=index, operand=operand, condition=condition, uuid=id
        )
