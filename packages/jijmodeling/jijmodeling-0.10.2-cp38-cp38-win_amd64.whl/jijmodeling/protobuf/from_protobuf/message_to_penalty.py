import jijmodeling_schema as pb

from jijmodeling.expression.constraint import Penalty
from jijmodeling.protobuf.from_protobuf.message_to_expression import (
    message_to_expression,
)
from jijmodeling.protobuf.from_protobuf.message_to_forall import message_to_forall


def message_to_penalty(penalty: pb.Penalty) -> Penalty:
    """
    Convert a `Penalty` message into a `Penalty` object.

    Args:
        penalty (pb.Penalty): a `Penalty` message

    Returns:
        Penalty: a `Penalty` object
    """
    # Set the name of the penalty.
    name = penalty.name

    # Set the penalty term.
    expr = message_to_expression(penalty.expression)

    # Set the list of forall.
    forall = [message_to_forall(forall) for forall in penalty.forall]

    return Penalty(
        label=name,
        penalty_term=expr,
        forall=forall,
        with_multiplier=penalty.needs_multiplier,
    )
