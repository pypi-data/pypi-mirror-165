import jijmodeling_schema as pb

from jijmodeling.expression.variables.variable import Element


def element_to_message(element: Element) -> pb.Expression:
    """
    Convert an `Element` object to an `Element` message.

    Args:
        element (Element): an `Element` object

    Returns:
        pb.Expression: an `Element` message
    """
    # Create an empty `ArrayShape` message.
    element_message = pb.Element()

    # Set the symbol
    element_message.symbol = element.label

    # Create an empty `Expression` message.
    message = pb.Expression()

    # Set the id that the `Element` object has.
    message.id = element.uuid

    # Set the kind of nodes to an `ArrayShape` message.
    message.kind.element = element_message

    # NOTE: Import a module within a local scope to fix a circular import.
    # - https://stackoverflow.com/questions/59462679/design-of-python-conditional-imports
    # - https://medium.com/@hamana.hadrien/so-you-got-a-circular-import-in-python-e9142fe10591
    from jijmodeling.protobuf.to_protobuf.expression_to_message import (
        expression_to_message,
    )

    # Set the parent of the `Element` object.
    message.children.append(expression_to_message(element.parent))

    return message
