import jijmodeling_schema as pb

from jijmodeling.expression.variables.variable import Subscripts


def subscript_op_to_message(subscript_op: Subscripts) -> pb.Expression:
    """
    Convert a `Subscripts` object to a `SubscriptOp` message.

    Args:
        subscript_op (Subscripts): a `Subscripts` object.

    Returns:
        pb.Expression: an `Expression` message.
    """
    # Create an empty `SubscriptOp` message.
    subscript_op_message = pb.SubscriptOp()

    # Set length of the subscripts.
    subscript_op_message.num_subs = len(subscript_op.subscripts)

    # Create an empty `Expression` message.
    message = pb.Expression()

    # Set the id that the `Expression` object has.
    message.id = subscript_op.uuid

    # Set the kind of nodes to an `BinaryOp` message.
    message.kind.subscript_op = subscript_op_message

    # NOTE: Import a module within a local scope to fix a circular import.
    # - https://stackoverflow.com/questions/59462679/design-of-python-conditional-imports
    # - https://medium.com/@hamana.hadrien/so-you-got-a-circular-import-in-python-e9142fe10591
    from jijmodeling.protobuf.to_protobuf.expression_to_message import (
        expression_to_message,
    )

    # Set the target array object.
    message.children.append(expression_to_message(subscript_op.variable))

    # Set the subscripts.
    message.children.extend(
        [expression_to_message(expr) for expr in subscript_op.subscripts]
    )

    return message
