import jijmodeling_schema as pb

from jijmodeling.expression.variables.placeholders import ArrayShape, Placeholder


def placeholder_to_message(placeholder: Placeholder) -> pb.Expression:
    """
    Convert a `Placeholder` object to an `Expression` message.

    Args:
        placeholder (Placeholder): a `Placeholder` object

    Returns:
        pb.Expression: an `Expression` message
    """
    # Create an empty `Placeholder` message.
    placeholder_message = pb.Placeholder()

    # Set the symbol.
    placeholder_message.symbol = placeholder.label

    # Set the number of dimensions.
    placeholder_message.dim = placeholder.dim

    # Create an empty `Expression` message.
    message = pb.Expression()

    # Set the id that the `Placeholder` object has.
    message.id = placeholder.uuid

    # Set the shape
    for shape in placeholder.shape:
        # Case: number of elements is variadic.
        if type(shape) is ArrayShape:
            # Set the kind of the element of the shape.
            placeholder_message.shape.append(pb.PlaceholderShapeElement.DYNAMIC)
        # Case: number of elements is fixed.
        else:
            # Set the kind of the element of the shape.
            placeholder_message.shape.append(pb.PlaceholderShapeElement.EXPRESSION)

            # NOTE: Import a module within a local scope to fix a circular import.
            # - https://stackoverflow.com/questions/59462679/design-of-python-conditional-imports
            # - https://medium.com/@hamana.hadrien/so-you-got-a-circular-import-in-python-e9142fe10591
            from jijmodeling.protobuf.to_protobuf.expression_to_message import (
                expression_to_message,
            )

            # Set the shape
            message.children.append(expression_to_message(shape))

    # Set the kind of nodes to a `Placeholder` message.
    message.kind.placeholder = placeholder_message

    # Serialize the `Expression` object into a bytes object.
    return message
