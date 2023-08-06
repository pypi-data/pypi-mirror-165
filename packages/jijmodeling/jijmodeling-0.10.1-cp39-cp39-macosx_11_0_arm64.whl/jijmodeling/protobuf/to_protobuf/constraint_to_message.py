import jijmodeling_schema as pb

from ulid import ULID

from jijmodeling.expression.constraint import Constraint
from jijmodeling.protobuf.to_protobuf.expression_to_message import expression_to_message
from jijmodeling.protobuf.to_protobuf.forall_to_message import forall_to_message


def constraint_to_message(constraint: Constraint) -> pb.Constraint:
    """
    Convert a `Constraint` object into a `Constraint` message.

    Args:
        constraint (Constraint): a `Constraint` object

    Returns:
        pb.Constraint: a `Constraint` message
    """
    # Create an empty `Constraint` message.
    message = pb.Constraint()

    # Set the id of the constraint.
    message.id = str(ULID())

    # Set the name of the constraint.
    message.name = constraint.label

    # Set the expression of the constraint.
    message.expression = expression_to_message(constraint.condition)

    # Set the list of forall.
    message.forall.extend(
        [
            forall_to_message(element, condition)
            for element, condition in constraint.forall
        ]
    )

    # Set the left_lower.
    if constraint.left_lower is not None:
        message.left_lower = expression_to_message(constraint.left_lower)

    message.is_penalty = constraint.with_penalty

    message.needs_multiplier = constraint.with_multiplier

    message.needs_square = constraint.auto_qubo

    return message
