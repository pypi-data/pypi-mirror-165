import jijmodeling_schema as pb

from jijmodeling.problem.problem import Problem, ProblemSense
from jijmodeling.protobuf.from_protobuf.message_to_constraint import (
    message_to_constraint,
)
from jijmodeling.protobuf.from_protobuf.message_to_expression import (
    message_to_expression,
)
from jijmodeling.protobuf.from_protobuf.message_to_penalty import message_to_penalty


def message_to_problem(problem: pb.Problem) -> Problem:
    """
    Convert a `Problem` message into a `Problem` object.

    Args:
        problem (pb.Problem): a `Problem` message

    Returns:
        Problem: a `Problem` object
    """
    # Set sense of the problem.
    if problem.sense == pb.ProblemSense.MIN:
        sense = ProblemSense.MINIMUM
    else:
        sense = ProblemSense.MAXIMUM

    # Set the objective function.
    objective = message_to_expression(problem.objective)

    # Set the constraints.
    constraints = {
        constraint.name: message_to_constraint(constraint)
        for constraint in problem.constraints
    }

    # Set the penalties.
    penalties = {
        penalty.name: message_to_penalty(penalty) for penalty in problem.penalties
    }

    return Problem(
        name=problem.name,
        sense=sense,
        objective=objective,
        constraints=constraints,
        penalties=penalties,
    )
