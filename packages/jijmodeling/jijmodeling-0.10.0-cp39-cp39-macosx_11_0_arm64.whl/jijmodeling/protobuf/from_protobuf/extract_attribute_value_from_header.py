from typing import Union

import jijmodeling_schema as pb


def extract_attribute_value_from_header(
    bytes: bytes,
) -> Union[pb.Problem, pb.Expression]:
    """
    Extract the attribute value from a header messsage.

    Args:
        bytes (bytes): a bytes object that can be decoded in the `Header` message

    Returns:
        Union[pb.Problem, pb.Expression]: an instance object of either `Problem` message class or `Expression` message class
    """
    # Convert the bytes object into the `Header` message object.
    header = pb.Header.FromString(bytes)

    # Extract the attribute value from the header message.
    attribute_value = pb.betterproto.which_one_of(header.value, "value")[1]

    return attribute_value
