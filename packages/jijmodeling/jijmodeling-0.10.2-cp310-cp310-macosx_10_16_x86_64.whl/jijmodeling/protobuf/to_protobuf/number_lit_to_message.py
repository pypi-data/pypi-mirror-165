import struct

import jijmodeling_schema as pb

from jijmodeling.expression.expression import DataType, Number


def number_lit_to_message(lit: Number) -> pb.Expression:
    """
    Convert a `Number` object to an `Expression` message.

    Args:
        lit (Number): a `Number` object

    Returns:
        jijmodeling_schema.Expression: an `Expression` message
    """
    # Create an empty `NumberLit` message.
    number_lit = pb.NumberLit()

    # Set the type of the value that the `Number` object has.
    # Case: int
    if lit.dtype == DataType.INT:
        number_lit.type = pb.NumberLitType.INTEGER

        # Set the value that the `Number` object has.
        # Convert the value to the bytes object.
        number_lit.value = int.from_bytes(struct.pack(">q", lit.value), "big")
    # Case: float
    elif lit.dtype == DataType.FLOAT:
        number_lit.type = pb.NumberLitType.FLOAT

        # Set the value that the `Number` object has.
        # Convert the value to the bytes object.
        number_lit.value = int.from_bytes(struct.pack(">d", lit.value), "big")
    # Otherwise
    else:
        number_lit.type = pb.NumberLitType.UNKNOWN

    # Create an empty `Expression` message.
    message = pb.Expression()

    # Set the id that the `Number` object has.
    message.id = lit.uuid

    # Set the kind of nodes to `NumberLit`.
    message.kind.number_lit = number_lit

    # Serialize the `Expression` object into a bytes object.
    return message
