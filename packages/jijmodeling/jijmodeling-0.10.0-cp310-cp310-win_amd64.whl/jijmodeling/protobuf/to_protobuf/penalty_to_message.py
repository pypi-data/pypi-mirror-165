import jijmodeling_schema as pb

from ulid import ULID

from jijmodeling.expression.constraint import Penalty
from jijmodeling.protobuf.to_protobuf.expression_to_message import expression_to_message
from jijmodeling.protobuf.to_protobuf.forall_to_message import forall_to_message


def penalty_to_message(penalty: Penalty) -> pb.Penalty:
    """
    Convert a `Penalty` object into a `Penalty` message.

    Args:
        penalty (Penalty): a `Penalty` object

    Returns:
        pb.Penalty: a `Penalty` message
    """
    # Create an empty `Penalty` message
    message = pb.Penalty()

    # Set the id of the penalty.
    message.id = str(ULID())

    # Set the name of the penalty.
    message.name = penalty.label

    # Set the penalty term.
    message.expression = expression_to_message(penalty.penalty_term)

    # Set the list of forall.
    message.forall.extend(
        [forall_to_message(element, condition) for element, condition in penalty.forall]
    )

    # Set the needs_multiplier
    message.needs_multiplier = penalty.with_multiplier

    return message
