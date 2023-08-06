import jijmodeling_schema as pb

from jijmodeling.expression.mathfunc import (
    AbsoluteValue,
    Ceil,
    Floor,
    Log2,
    UnaryOperator,
)


def unary_op_to_message(unary_op: UnaryOperator) -> pb.Expression:
    """
    Convert a `UnaryOperator` object to an `Expression` message.

    Args:
        unary_op (UnaryOperator): a `UnaryOperator` object

    Returns:
        pb.Expression: an `Expression` message
    """
    # Create an empty `UnaryOp` message.
    unary_op_message = pb.UnaryOp()

    # Set the kind of the unary operator node.
    if type(unary_op) is AbsoluteValue:
        unary_op_message.kind = pb.UnaryOpKind.ABS
    elif type(unary_op) is Ceil:
        unary_op_message.kind = pb.UnaryOpKind.CEIL
    elif type(unary_op) is Floor:
        unary_op_message.kind = pb.UnaryOpKind.FLOOR
    elif type(unary_op) is Log2:
        unary_op_message.kind = pb.UnaryOpKind.LOG2
    else:
        raise TypeError(f"{unary_op.__class__.__name__} is not supported")

    # Create an empty `Expression` message.
    message = pb.Expression()

    # Set the id that the `Expression` object has.
    message.id = unary_op.uuid

    # Set the kind of nodes to an `UnaryOp` message.
    message.kind.unary_op = unary_op_message

    # NOTE: Import a module within a local scope to fix a circular import.
    # - https://stackoverflow.com/questions/59462679/design-of-python-conditional-imports
    # - https://medium.com/@hamana.hadrien/so-you-got-a-circular-import-in-python-e9142fe10591
    from jijmodeling.protobuf.to_protobuf.expression_to_message import (
        expression_to_message,
    )

    # Set the operand of the `UnaryOperator` object.
    message.children.append(expression_to_message(unary_op.operand))

    return message
