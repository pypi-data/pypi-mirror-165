import jijmodeling_schema as pb

from jijmodeling.expression.variables.deci_vars import Binary


def binary_var_to_message(binary_var: Binary) -> pb.Expression:
    """
    Convert a `Binary` object to an `BinaryVar` message.

    Args:
        binary_var (Binary): a `Binary` object.

    Returns:
        pb.Expression: an `Expression` message.
    """
    # Create an empty `BinaryVar` message.
    binary_var_message = pb.BinaryVar()

    # Set the symbol.
    binary_var_message.symbol = binary_var.label

    # Set length of the shape.
    binary_var_message.dim = binary_var.dim

    # Create an empty `Expression` message.
    message = pb.Expression()

    # Set the id that the `Binary` object has.
    message.id = binary_var.uuid

    # Set the kind of nodes to a `BinaryVar` message.
    message.kind.binary_var = binary_var_message

    # NOTE: Import a module within a local scope to fix a circular import.
    # - https://stackoverflow.com/questions/59462679/design-of-python-conditional-imports
    # - https://medium.com/@hamana.hadrien/so-you-got-a-circular-import-in-python-e9142fe10591
    from jijmodeling.protobuf.to_protobuf.expression_to_message import (
        expression_to_message,
    )

    # Set the shape.
    message.children = [
        expression_to_message(shape_element) for shape_element in binary_var.shape
    ]

    # Serialize the `Expression` object into a bytes object.
    return message
