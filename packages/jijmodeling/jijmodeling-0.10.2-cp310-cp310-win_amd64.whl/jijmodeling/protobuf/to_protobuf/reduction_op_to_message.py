import jijmodeling_schema as pb

from jijmodeling.expression.condition import NoneCondition
from jijmodeling.expression.prod import ProdOperator
from jijmodeling.expression.sum import ReductionOperator, SumOperator


def reduction_op_to_message(reduction_op: ReductionOperator) -> pb.Expression:
    """
    Convert a `ReductionOperator` object to a `ReductionOp` message.

    Args:
        reduction_op (ReductionOperator): a `ReductionOperator` object.

    Raises:
        TypeError: the error occurs if the kind of the reduction operator is not supported

    Returns:
        pb.Expression: an `Expression` message.
    """
    # Create an empty `ReductionOp` message.
    reduction_op_message = pb.ReductionOp()

    # Set the kind of the `ReductionOp`.
    if type(reduction_op) is SumOperator:
        reduction_op_message.kind = pb.ReductionOpKind.SUM
    elif type(reduction_op) is ProdOperator:
        reduction_op_message.kind = pb.ReductionOpKind.PROD
    else:
        raise TypeError(f"{reduction_op.__class__.__name__} is not supported.")

    # Create an empty `Expression` message.
    message = pb.Expression()

    # Set the id that the `Expression` object has.
    message.id = reduction_op.uuid

    # NOTE: Import a module within a local scope to fix a circular import.
    # - https://stackoverflow.com/questions/59462679/design-of-python-conditional-imports
    # - https://medium.com/@hamana.hadrien/so-you-got-a-circular-import-in-python-e9142fe10591
    from jijmodeling.protobuf.to_protobuf.expression_to_message import (
        expression_to_message,
    )

    # Set the index.
    message.children.append(expression_to_message(reduction_op.sum_index))

    # Set the operand.
    message.children.append(expression_to_message(reduction_op.operand))

    # Set the condition expression if the `ReductionOp` object has it.
    if type(reduction_op.condition) is NoneCondition:
        reduction_op_message.has_condition = False
    else:
        reduction_op_message.has_condition = True
        # Set the condition expression
        message.children.append(expression_to_message(reduction_op.condition))

    # Set the kind of nodes to an `ReductionOp` message.
    message.kind.reduction_op = reduction_op_message

    return message
