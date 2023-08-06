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


def binary_op_to_message(
    binary_op: Union[BinaryOperator, Range, Condition]
) -> pb.Expression:
    """
    Convert a `BinaryOperator | Range | Condition` object to an `Expression`.

    message.

    Args:
        unary_op (BinaryOperator): an expression node that has two children

    Returns:
        pb.Expression: an `Expression` message
    """
    # Create an empty `BinaryOp` message.
    binary_op_message = pb.BinaryOp()

    # Set the kind of the binary operator node.
    # BinaryOp
    if type(binary_op) is Add:
        binary_op_message.kind = pb.BinaryOpKind.ADD
    elif type(binary_op) is Mul:
        binary_op_message.kind = pb.BinaryOpKind.MUL
    elif type(binary_op) is Div:
        binary_op_message.kind = pb.BinaryOpKind.DIV
    elif type(binary_op) is Power:
        binary_op_message.kind = pb.BinaryOpKind.POW
    elif type(binary_op) is Mod:
        binary_op_message.kind = pb.BinaryOpKind.MOD
    # Range
    elif type(binary_op) is Range:
        binary_op_message.kind = pb.BinaryOpKind.RANGE
    # ComparisonOp
    elif type(binary_op) is Equal:
        binary_op_message.kind = pb.BinaryOpKind.EQ
    elif type(binary_op) is NotEqual:
        binary_op_message.kind = pb.BinaryOpKind.NOT_EQ
    elif type(binary_op) is LessThan:
        binary_op_message.kind = pb.BinaryOpKind.LESS_THAN
    elif type(binary_op) is LessThanEqual:
        binary_op_message.kind = pb.BinaryOpKind.LESS_THAN_EQ
    # LogicalOp
    elif type(binary_op) is AndOperator:
        binary_op_message.kind = pb.BinaryOpKind.AND
    elif type(binary_op) is OrOperator:
        binary_op_message.kind = pb.BinaryOpKind.OR
    elif type(binary_op) is XorOperator:
        binary_op_message.kind = pb.BinaryOpKind.XOR
    # Otherwise
    else:
        raise TypeError(f"{binary_op.__class__.__name__} is not supported")

    # Create an empty `Expression` message.
    message = pb.Expression()

    # Set the id that the `Expression` object has.
    message.id = binary_op.uuid

    # Set the kind of nodes to the `BinaryOp` message.
    message.kind.binary_op = binary_op_message

    # NOTE: Import a module within a local scope to fix a circular import.
    # - https://stackoverflow.com/questions/59462679/design-of-python-conditional-imports
    # - https://medium.com/@hamana.hadrien/so-you-got-a-circular-import-in-python-e9142fe10591
    from jijmodeling.protobuf.to_protobuf.expression_to_message import (
        expression_to_message,
    )

    if type(binary_op) is Range:
        # Set the range of the `Range` object.
        message.children.append(expression_to_message(binary_op.start))
        message.children.append(expression_to_message(binary_op.last))
    elif isinstance(binary_op, (BinaryOperator, Condition)):
        # Set the children of the `BinaryOperator` object.
        message.children.append(expression_to_message(binary_op.left))
        message.children.append(expression_to_message(binary_op.right))
    # Otherwise
    else:
        raise TypeError(f"{binary_op.__class__.__name__} is not supported")

    return message
