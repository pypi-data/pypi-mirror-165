from typing import Union

from jijmodeling.expression.condition import Condition
from jijmodeling.expression.expression import Expression
from jijmodeling.expression.variables.variable import Range
from jijmodeling.problem.problem import Problem
from jijmodeling.protobuf.to_protobuf.add_header_to_message import add_header_to_message
from jijmodeling.protobuf.to_protobuf.expression_to_message import expression_to_message
from jijmodeling.protobuf.to_protobuf.problem_to_message import problem_to_message


def to_protobuf(object: Union[Expression, Range, Condition, Problem]) -> bytes:
    """
    Convert a JijModeling's object to a bytes object serialized by protobuf.

    Args:
        expr (Expression): a instance object of the `Expression` class

    Raises:
        TypeError: The error raises if the instance object cannot be converted to a protobuf object

    Returns:
        bytes: a bytes object
    """
    if isinstance(object, (Expression, Range, Condition)):
        message = add_header_to_message(expression_to_message(object))
        return bytes(message)
    elif isinstance(object, Problem):
        message = add_header_to_message(problem_to_message(object))
        return bytes(message)
    else:
        raise TypeError(
            f"{object.__class__.__name__} is not an {Expression.__name__} instance object."
        )
