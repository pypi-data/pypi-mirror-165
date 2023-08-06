from typing import Union

import jijmodeling_schema as pb

from jijmodeling.expression.expression import Expression
from jijmodeling.problem.problem import Problem
from jijmodeling.protobuf.from_protobuf.extract_attribute_value_from_header import (
    extract_attribute_value_from_header,
)
from jijmodeling.protobuf.from_protobuf.message_to_expression import (
    message_to_expression,
)
from jijmodeling.protobuf.from_protobuf.message_to_problem import message_to_problem


def from_protobuf(bytes: bytes) -> Union[Problem, Expression]:
    """
    Convert a bytes object in protobuf to a JijModeling's object.

    Args:
        bytes (bytes): a bytes object in protobuf

    Returns:
        Expression: an expression
    """
    # Convert the bytes object into the message object.
    attribute_value = extract_attribute_value_from_header(bytes)

    if type(attribute_value) is pb.Problem:
        return message_to_problem(attribute_value)
    elif isinstance(attribute_value, pb.Expression):
        return message_to_expression(attribute_value)
    else:
        raise RuntimeError(
            f"cannot convert the bytes object into the instance object according to the class in JijModeling (bytes = {str(bytes)})"
        )
