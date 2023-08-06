import jijmodeling_schema as pb

from jijmodeling.expression.variables.jagged_array import JaggedArray


def message_to_jagged_array(id: str, message: pb.JaggedArray) -> JaggedArray:
    """
    Convert a message to a `JaggedArray` object.

    Args:
        id (str): the id of the `JaggedArray` object
        message (pb.JaggedArray): the `JaggedArray` message

    Returns:
        JaggedArray: a `JaggedArray` object
    """
    # Set the symbol.
    symbol = message.symbol

    # Set the number of dimensions.
    dim = message.dim

    return JaggedArray(label=symbol, dim=dim, uuid=id)
