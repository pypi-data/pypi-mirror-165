import jijmodeling_schema as pb

from jijmodeling.expression.variables.jagged_array import JaggedArray


def jagged_array_to_message(jagged_array: JaggedArray) -> pb.Expression:
    """
    Convert a `JaggedArray` object to a `JaggedArray` message.

    Args:
        jagged_array (JaggedArray): a `JaggedArray` object

    Returns:
        pb.Expression: a `JaggedArray` object
    """
    # Create an empty `JaggedArray` message.
    jagged_array_message = pb.JaggedArray()

    # Set the symbol.
    jagged_array_message.symbol = jagged_array.label

    # Set the number of dimensions.
    jagged_array_message.dim = jagged_array.dim

    # Create an empty `Expression` message.
    message = pb.Expression()

    # Set the id that the `JaggedArray` object has.
    message.id = jagged_array.uuid

    # Set the kind of nodes to a `JaggedArray` message.
    message.kind.jagged_array = jagged_array_message

    # Serialize the `Expression` object into a bytes object.
    return message
