import jijmodeling_schema as pb

from jijmodeling.expression.constraint import Constraint
from jijmodeling.protobuf.from_protobuf.message_to_expression import (
    message_to_expression,
)
from jijmodeling.protobuf.from_protobuf.message_to_forall import message_to_forall


def message_to_constraint(constraint: pb.Constraint) -> Constraint:
    """
    Convert a `Constraint` message into a `Constraint` object.

    Args:
        constraint (pb.Constraint): a `Constraint` message

    Returns:
        Constraint: a `Constraint` object
    """
    # Set the name of the constraint.
    name = constraint.name

    # Set the condition expression.
    condition = message_to_expression(constraint.expression)

    # Set the list of forall.
    forall = [message_to_forall(forall) for forall in constraint.forall]

    # Set the left_lower.
    has_left_lower = (
        pb.betterproto.which_one_of(constraint.left_lower.kind, "kind")[1] is not None
    )
    if has_left_lower:
        left_lower = message_to_expression(constraint.left_lower)
    else:
        left_lower = None

    return Constraint(
        label=name,
        condition=condition,
        forall=forall,
        left_lower=left_lower,
        with_penalty=constraint.is_penalty,
        with_multiplier=constraint.needs_multiplier,
        auto_qubo=constraint.needs_square,
    )
