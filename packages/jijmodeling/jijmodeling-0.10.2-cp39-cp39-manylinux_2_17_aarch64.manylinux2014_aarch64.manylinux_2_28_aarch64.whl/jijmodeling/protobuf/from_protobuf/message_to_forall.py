from typing import Optional, Tuple

import jijmodeling_schema as pb

from jijmodeling.expression.condition import Condition
from jijmodeling.expression.variables.variable import Element
from jijmodeling.protobuf.from_protobuf.message_to_expression import (
    message_to_expression,
)


def message_to_forall(forall: pb.Forall) -> Tuple[Element, Optional[Condition]]:
    """
    Convert a `Forall` message into a `forall` object.

    Args:
        forall (pb.Forall): a `Forall` message

    Returns:
        Tuple[Element, Optional[Condition]]: objects to make the `forall` object
    """
    # Set the element.
    element = message_to_expression(forall.element)

    # Set the condition expression.
    is_none_condition = (
        pb.betterproto.which_one_of(forall.condition.kind, "kind")[1] is None
    )
    condition = None if is_none_condition else message_to_expression(forall.condition)

    return (element, condition)
