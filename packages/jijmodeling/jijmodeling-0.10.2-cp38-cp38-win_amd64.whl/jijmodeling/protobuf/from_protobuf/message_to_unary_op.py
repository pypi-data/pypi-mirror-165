import jijmodeling_schema as pb

from jijmodeling.expression.mathfunc import (
    AbsoluteValue,
    Ceil,
    Floor,
    Log2,
    UnaryOperator,
)


def message_to_unary_op(
    id: str, message: pb.UnaryOp, operand: pb.Expression
) -> UnaryOperator:
    """
    Convert a message to a `UnaryOperator` object.

    Args:
        id (str): the id of the `UnaryOperator` object
        message (pb.UnaryOp): the `UnaryOp` message
        operand (pb.Expression): the operand node that the `UnaryOp` message has

    Raises:
        TypeError: the error happens if the message cannot be converted to a `UnaryOperator` object

    Returns:
        UnaryOperator: a `UnaryOperator` object
    """
    # NOTE: Import a module within a local scope to fix a circular import.
    # - https://stackoverflow.com/questions/59462679/design-of-python-conditional-imports
    # - https://medium.com/@hamana.hadrien/so-you-got-a-circular-import-in-python-e9142fe10591
    from jijmodeling.protobuf.from_protobuf.message_to_expression import (
        message_to_expression,
    )

    if message.kind == pb.UnaryOpKind.ABS:
        return AbsoluteValue(uuid=id, operand=message_to_expression(operand))
    elif message.kind == pb.UnaryOpKind.CEIL:
        return Ceil(uuid=id, operand=message_to_expression(operand))
    elif message.kind == pb.UnaryOpKind.FLOOR:
        return Floor(uuid=id, operand=message_to_expression(operand))
    elif message.kind == pb.UnaryOpKind.LOG2:
        return Log2(uuid=id, operand=message_to_expression(operand))
    else:
        raise TypeError(f"cannot convert the unary operator to an expression")
