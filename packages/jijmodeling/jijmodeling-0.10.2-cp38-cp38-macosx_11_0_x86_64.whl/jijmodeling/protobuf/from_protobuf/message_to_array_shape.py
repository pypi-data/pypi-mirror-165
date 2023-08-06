import jijmodeling_schema as pb

from jijmodeling.expression.variables.placeholders import ArrayShape


def message_to_array_shape(
    id: str, message: pb.ArrayShape, array: pb.Expression
) -> ArrayShape:
    """
    Convert a message to a `ArrayShape` object.

    Args:
        id (str): the id of the `ArrayShape` object
        message (pb.ArrayShape): the `ArrayShape` message
        array (pb.Expression): the target array of the array shape

    Returns:
        ArrayShape: an `ArrayShape` object
    """
    # Set the number of axis.
    axis = message.axis

    # NOTE: Import a module within a local scope to fix a circular import.
    # - https://stackoverflow.com/questions/59462679/design-of-python-conditional-imports
    # - https://medium.com/@hamana.hadrien/so-you-got-a-circular-import-in-python-e9142fe10591
    from jijmodeling.protobuf.from_protobuf.message_to_expression import (
        message_to_expression,
    )

    # Set the target array of this array shape.
    array = message_to_expression(array)

    return ArrayShape(uuid=id, array=array, dimension=axis)
