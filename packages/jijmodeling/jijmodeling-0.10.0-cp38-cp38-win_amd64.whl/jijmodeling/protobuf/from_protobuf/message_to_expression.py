from typing import Union

import jijmodeling_schema as pb

from jijmodeling.expression.condition import Condition
from jijmodeling.expression.expression import Expression
from jijmodeling.expression.variables.variable import Range
from jijmodeling.protobuf.from_protobuf.message_to_array_shape import (
    message_to_array_shape,
)
from jijmodeling.protobuf.from_protobuf.message_to_binary_op import message_to_binary_op
from jijmodeling.protobuf.from_protobuf.message_to_binary_var import (
    message_to_binary_var,
)
from jijmodeling.protobuf.from_protobuf.message_to_element import message_to_element
from jijmodeling.protobuf.from_protobuf.message_to_integer_var import (
    message_to_integer_var,
)
from jijmodeling.protobuf.from_protobuf.message_to_jagged_array import (
    message_to_jagged_array,
)
from jijmodeling.protobuf.from_protobuf.message_to_number_lit import (
    message_to_number_lit,
)
from jijmodeling.protobuf.from_protobuf.message_to_placeholder import (
    message_to_placeholder,
)
from jijmodeling.protobuf.from_protobuf.message_to_reduction_op import (
    message_to_reduction_op,
)
from jijmodeling.protobuf.from_protobuf.message_to_subscript_op import (
    message_to_subscript_op,
)
from jijmodeling.protobuf.from_protobuf.message_to_unary_op import message_to_unary_op


def message_to_expression(
    expression: pb.Expression,
) -> Union[Expression, Range, Condition]:
    """
    Convert a message object to a `Expression` object.

    Args:
        expression (pb.Expression): a `Expression` message

    Raises:
        RuntimeError: the error occurs if the massage cannot be converted to an object that is a subclass of the `Expression` class

    Returns:
        Expression: an instance object that is a subclass of the `Expression` class
    """
    # Get the id that the message has.
    id = expression.id

    # Get the `Expression` object from the field inside the oneof.
    expr_attr = pb.betterproto.which_one_of(expression.kind, "kind")[1]

    if type(expr_attr) is pb.NumberLit:
        return message_to_number_lit(id, expr_attr)
    elif type(expr_attr) is pb.Placeholder:
        shape = expression.children
        return message_to_placeholder(id, expr_attr, shape)
    elif type(expr_attr) is pb.ArrayShape:
        array = expression.children[0]
        return message_to_array_shape(id, expr_attr, array)
    elif type(expr_attr) is pb.Element:
        parent = expression.children[0]
        return message_to_element(id, expr_attr, parent)
    elif type(expr_attr) is pb.JaggedArray:
        return message_to_jagged_array(id, expr_attr)
    elif type(expr_attr) is pb.BinaryVar:
        shape = expression.children
        return message_to_binary_var(id, expr_attr, shape)
    elif type(expr_attr) is pb.IntegerVar:
        return message_to_integer_var(id, expr_attr, expression.children)
    elif type(expr_attr) is pb.UnaryOp:
        operand = expression.children[0]
        return message_to_unary_op(id, expr_attr, operand)
    elif type(expr_attr) is pb.BinaryOp:
        left = expression.children[0]
        right = expression.children[1]
        return message_to_binary_op(id, expr_attr, left, right)
    elif type(expr_attr) is pb.SubscriptOp:
        return message_to_subscript_op(id, expr_attr, expression.children)
    elif type(expr_attr) is pb.ReductionOp:
        return message_to_reduction_op(id, expr_attr, expression.children)
    else:
        raise RuntimeError(
            f"cannot convert the {expr_attr.__class__.__name__} object into the instance object according to the class in JijModeling"
        )
