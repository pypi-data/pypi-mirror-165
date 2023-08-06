import jijmodeling_schema as pb

from jijmodeling.expression.condition import Condition, NoneCondition
from jijmodeling.expression.variables.variable import Element
from jijmodeling.protobuf.to_protobuf.element_to_message import element_to_message
from jijmodeling.protobuf.to_protobuf.expression_to_message import expression_to_message


def forall_to_message(element: Element, condition: Condition) -> pb.Forall:
    """
    Convert a `forall` object into a `Forall` message.

    Args:
        element (Element): an `Element` object
        condition (Condition): a `Condition` object

    Returns:
        pb.Forall: a `Forall` message
    """
    # Create an empty `Forall` message.
    message = pb.Forall()

    # Set the element.
    message.element = element_to_message(element)

    # Set the condition expression for the element.
    if type(condition) is not NoneCondition:
        message.condition = expression_to_message(condition)

    return message
