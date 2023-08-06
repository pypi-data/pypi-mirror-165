import jijmodeling_schema as pb

from jijmodeling.expression.variables.placeholders import ArrayShape


def array_shape_to_message(array_shape: ArrayShape) -> pb.Expression:
    """
    Convert an `ArrayShape` object to an `Expression` message.

    Args:
        array_shape (ArrayShape): an `ArrayShape` object

    Returns:
        pb.Expression: an `Expression` message
    """
    # Create an empty `ArrayShape` message.
    array_shape_message = pb.ArrayShape()

    # Set the number of axis
    array_shape_message.axis = array_shape.dimension

    # Create an empty `Expression` message.
    message = pb.Expression()

    # Set the id that the `ArrayShape` object has.
    message.id = array_shape.uuid

    # Set the kind of nodes to an `ArrayShape` message.
    message.kind.array_shape = array_shape_message

    # NOTE: Import a module within a local scope to fix a circular import.
    # - https://stackoverflow.com/questions/59462679/design-of-python-conditional-imports
    # - https://medium.com/@hamana.hadrien/so-you-got-a-circular-import-in-python-e9142fe10591
    from jijmodeling.protobuf.to_protobuf.expression_to_message import (
        expression_to_message,
    )

    # Set the array of the ArrayShape.
    message.children.append(expression_to_message(array_shape.array))

    return message
