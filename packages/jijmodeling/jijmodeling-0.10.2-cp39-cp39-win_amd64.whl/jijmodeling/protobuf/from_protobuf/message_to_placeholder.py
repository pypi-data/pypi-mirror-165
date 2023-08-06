from typing import List

import jijmodeling_schema as pb

from jijmodeling.expression.variables.placeholders import Placeholder


def message_to_placeholder(
    id: str, message: pb.Placeholder, shape: List[pb.Expression]
) -> Placeholder:
    """
    Convert a message to a `Placeholder` object.

    Args:
        id (str): the id of the `Placeholder` object
        message (pb.Placeholder): the `Placeholder` message
        shape (List[pb.Expression]): the shape of the `Placeholder` object

    Returns:
        Placeholder: a `Placeholder` object
    """
    # Set the symbol.
    symbol = message.symbol

    # Set the number of dimensions.
    dim = message.dim

    # Set the shape.
    shape_list = []
    expr_idx = 0
    for shape_elt in message.shape:
        if shape_elt == pb.PlaceholderShapeElement.DYNAMIC:
            shape_list.append(None)
        else:
            # NOTE: Import a module within a local scope to fix a circular import.
            # - https://stackoverflow.com/questions/59462679/design-of-python-conditional-imports
            # - https://medium.com/@hamana.hadrien/so-you-got-a-circular-import-in-python-e9142fe10591
            from jijmodeling.protobuf.from_protobuf.message_to_expression import (
                message_to_expression,
            )

            shape_list.append(message_to_expression(shape[expr_idx]))
            expr_idx = expr_idx + 1

    return Placeholder(label=symbol, dim=dim, uuid=id, shape=shape_list)
