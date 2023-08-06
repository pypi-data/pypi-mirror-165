import jijmodeling_schema as pb

from jijmodeling.expression.variables.variable import Element


def message_to_element(id: str, message: pb.Element, parent: pb.Expression) -> Element:
    """
    Convert a message to a `Element` object.

    Args:
        id (str): the id of the `Element` object
        message (pb.Element): the `Element` message
        parent (pb.Expression): the parent node that the `Element` message has

    Returns:
        Element: an `Element` object
    """
    # Set the symbol
    symbol = message.symbol

    # NOTE: Import a module within a local scope to fix a circular import.
    # - https://stackoverflow.com/questions/59462679/design-of-python-conditional-imports
    # - https://medium.com/@hamana.hadrien/so-you-got-a-circular-import-in-python-e9142fe10591
    from jijmodeling.protobuf.from_protobuf.message_to_expression import (
        message_to_expression,
    )

    return Element(label=symbol, parent=message_to_expression(parent), uuid=id)
