import jijmodeling_schema as pb

from jijmodeling.expression.variables.deci_vars import Integer


def integer_var_to_message(integer_var: Integer) -> pb.Expression:
    """
    Convert an `Integer` object to an `IntegerVar` message.

    Args:
        integer_var (Integer): an `Integer` object.

    Returns:
        pb.Expression: an `Expression` message.
    """
    # Create an empty `IntegerVar` message.
    integer_var_message = pb.IntegerVar()

    # Set the symbol
    integer_var_message.symbol = integer_var.label
    # Set length of the shape
    integer_var_message.dim = integer_var.dim

    # Create an empty `Expression` message.
    message = pb.Expression()

    # Set the id that the `Integer` object has.
    message.id = integer_var.uuid

    # Set the kind of nodes to a `IntegerVar` message.
    message.kind.integer_var = integer_var_message

    # NOTE: Import a module within a local scope to fix a circular import.
    # - https://stackoverflow.com/questions/59462679/design-of-python-conditional-imports
    # - https://medium.com/@hamana.hadrien/so-you-got-a-circular-import-in-python-e9142fe10591
    from jijmodeling.protobuf.to_protobuf.expression_to_message import (
        expression_to_message,
    )

    # Set the bound of the `Integer` object.
    # lower bound
    message.children.append(expression_to_message(integer_var.lower))
    # upper bound
    message.children.append(expression_to_message(integer_var.upper))

    # Set the shape.
    message.children.extend(
        [expression_to_message(shape_element) for shape_element in integer_var.shape]
    )

    # Serialize the `Expression` object into a bytes object.
    return message
