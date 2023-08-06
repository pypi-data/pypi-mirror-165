from __future__ import annotations

from typing import Union

import jijmodeling_schema as pb

from jijmodeling.expression.condition import Condition
from jijmodeling.expression.expression import BinaryOperator, Expression, Number
from jijmodeling.expression.mathfunc import UnaryOperator
from jijmodeling.expression.sum import ReductionOperator
from jijmodeling.expression.variables.deci_vars import Binary, Integer
from jijmodeling.expression.variables.jagged_array import JaggedArray
from jijmodeling.expression.variables.placeholders import ArrayShape, Placeholder
from jijmodeling.expression.variables.variable import Element, Range, Subscripts
from jijmodeling.protobuf.to_protobuf.array_shape_to_message import (
    array_shape_to_message,
)
from jijmodeling.protobuf.to_protobuf.binary_op_to_message import binary_op_to_message
from jijmodeling.protobuf.to_protobuf.binary_var_to_message import binary_var_to_message
from jijmodeling.protobuf.to_protobuf.element_to_message import element_to_message
from jijmodeling.protobuf.to_protobuf.integer_var_to_message import (
    integer_var_to_message,
)
from jijmodeling.protobuf.to_protobuf.jagged_array_to_message import (
    jagged_array_to_message,
)
from jijmodeling.protobuf.to_protobuf.number_lit_to_message import number_lit_to_message
from jijmodeling.protobuf.to_protobuf.placeholder_to_message import (
    placeholder_to_message,
)
from jijmodeling.protobuf.to_protobuf.reduction_op_to_message import (
    reduction_op_to_message,
)
from jijmodeling.protobuf.to_protobuf.subscript_op_to_message import (
    subscript_op_to_message,
)
from jijmodeling.protobuf.to_protobuf.unary_op_to_message import unary_op_to_message


def expression_to_message(expr: Union[Expression, Range, Condition]) -> pb.Expression:
    """
    Convert a `Expression` instance object to an `Expression` message.

    Args:
        expr (Expression): an `Expression` instance object

    Raises:
        TypeError: the error occurs if the instance ofject cannot be converted to a protobuf object

    Returns:
        pb.Expression: a `Expression` message
    """
    if type(expr) is Number:
        message = number_lit_to_message(expr)
        return message
    elif type(expr) is Placeholder:
        message = placeholder_to_message(expr)
        return message
    elif type(expr) is ArrayShape:
        message = array_shape_to_message(expr)
        return message
    elif type(expr) is Element:
        message = element_to_message(expr)
        return message
    elif type(expr) is JaggedArray:
        message = jagged_array_to_message(expr)
        return message
    elif type(expr) is Binary:
        message = binary_var_to_message(expr)
        return message
    elif type(expr) is Integer:
        message = integer_var_to_message(expr)
        return message
    elif isinstance(expr, UnaryOperator):
        message = unary_op_to_message(expr)
        return message
    elif isinstance(expr, (BinaryOperator, Range, Condition)):
        message = binary_op_to_message(expr)
        return message
    elif type(expr) is Subscripts:
        message = subscript_op_to_message(expr)
        return message
    elif isinstance(expr, ReductionOperator):
        message = reduction_op_to_message(expr)
        return message
    else:
        raise TypeError(
            f"{expr.__class__.__name__} is not supported for converting it into a protobuf message."
        )
