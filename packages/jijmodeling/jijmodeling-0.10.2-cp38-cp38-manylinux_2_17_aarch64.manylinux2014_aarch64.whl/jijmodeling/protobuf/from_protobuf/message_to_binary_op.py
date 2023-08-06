from typing import Union

import jijmodeling_schema as pb

from jijmodeling.expression.condition import (
    AndOperator,
    Condition,
    Equal,
    LessThan,
    LessThanEqual,
    NotEqual,
    OrOperator,
    XorOperator,
)
from jijmodeling.expression.expression import Add, BinaryOperator, Div, Mod, Mul, Power
from jijmodeling.expression.variables.variable import Range


def message_to_binary_op(
    id: str, message: pb.BinaryOp, left: pb.Expression, right: pb.Expression
) -> Union[BinaryOperator, Range, Condition]:
    """
    Convert a message to a `BinaryOperator` object.

    Args:
        id (str): the id of the `BinaryOperator` object
        message (pb.BinaryOp): the `BinaryOp` message
        operand (pb.Expression): the operand node that the `BinaryOp` message has

    Raises:
        TypeError: the error happens if the message cannot be converted to a `BinaryOperator` object

    Returns:
        BinaryOperator: a `BinaryOperator` object
    """
    # NOTE: Import a module within a local scope to fix a circular import.
    # - https://stackoverflow.com/questions/59462679/design-of-python-conditional-imports
    # - https://medium.com/@hamana.hadrien/so-you-got-a-circular-import-in-python-e9142fe10591
    from jijmodeling.protobuf.from_protobuf.message_to_expression import (
        message_to_expression,
    )

    # Convert the children to the `Expression` objects.
    lhs = message_to_expression(left)
    rhs = message_to_expression(right)

    # BinaryOp
    if message.kind == pb.BinaryOpKind.ADD:
        return Add(uuid=id, left=lhs, right=rhs)
    elif message.kind == pb.BinaryOpKind.MUL:
        return Mul(uuid=id, left=lhs, right=rhs)
    elif message.kind == pb.BinaryOpKind.DIV:
        return Div(uuid=id, left=lhs, right=rhs)
    elif message.kind == pb.BinaryOpKind.POW:
        return Power(uuid=id, left=lhs, right=rhs)
    elif message.kind == pb.BinaryOpKind.MOD:
        return Mod(uuid=id, left=lhs, right=rhs)
    # Range
    elif message.kind == pb.BinaryOpKind.RANGE:
        return Range(start=lhs, last=rhs, uuid=id)
    # ComparisonOp
    elif message.kind == pb.BinaryOpKind.EQ:
        return Equal(uuid=id, left=lhs, right=rhs)
    elif message.kind == pb.BinaryOpKind.NOT_EQ:
        return NotEqual(uuid=id, left=lhs, right=rhs)
    elif message.kind == pb.BinaryOpKind.LESS_THAN:
        return LessThan(uuid=id, left=lhs, right=rhs)
    elif message.kind == pb.BinaryOpKind.LESS_THAN_EQ:
        return LessThanEqual(uuid=id, left=lhs, right=rhs)
    # Logicalop
    elif message.kind == pb.BinaryOpKind.AND:
        return AndOperator(uuid=id, left=lhs, right=rhs)
    elif message.kind == pb.BinaryOpKind.OR:
        return OrOperator(uuid=id, left=lhs, right=rhs)
    elif message.kind == pb.BinaryOpKind.XOR:
        return XorOperator(uuid=id, left=lhs, right=rhs)
    # Otherwise
    else:
        raise TypeError(
            f"cannot convert the binary operator (actual = {message}) to an expression."
        )
