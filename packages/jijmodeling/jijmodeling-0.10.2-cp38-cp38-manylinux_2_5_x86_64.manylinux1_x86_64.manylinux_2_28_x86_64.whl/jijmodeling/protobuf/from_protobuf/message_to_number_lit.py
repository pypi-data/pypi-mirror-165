import struct

import jijmodeling_schema as pb

from jijmodeling.expression.expression import DataType, Number


def message_to_number_lit(id: str, message: pb.NumberLit) -> Number:
    """
    Convert a message to a `Number` object.

    Args:
        message (pb.NumberLit): the `NumberLit` message
        id (str): the id of the `Number` object

    Returns:
        Number: a `Number` object
    """
    # Check the type that the number literal object has.
    # Case: integer
    if message.type == pb.NumberLitType.INTEGER:
        # Set the value type to `FLOAT`.
        dtype = DataType.INT
        # Set the integer value.
        value = struct.unpack(
            ">q",
            message.value.to_bytes(length=struct.calcsize(">q"), byteorder="big"),
        )[0]
    # Case: float
    elif message.type == pb.NumberLitType.FLOAT:
        # Set the value type to `FLOAT`.
        dtype = DataType.FLOAT
        # Convert the bits to a float value.
        value = struct.unpack(
            ">d",
            message.value.to_bytes(length=struct.calcsize(">d"), byteorder="big"),
        )[0]

    return Number(value=value, dtype=dtype, uuid=id)
