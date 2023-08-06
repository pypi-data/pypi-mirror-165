import jijmodeling_schema as pb

from ulid import ULID

from jijmodeling.problem.problem import Problem, ProblemSense
from jijmodeling.protobuf.to_protobuf.constraint_to_message import constraint_to_message
from jijmodeling.protobuf.to_protobuf.expression_to_message import expression_to_message
from jijmodeling.protobuf.to_protobuf.penalty_to_message import penalty_to_message


def problem_to_message(problem: Problem) -> pb.Problem:
    """
    Convert a `Problem` object into a `Problem` message.

    Args:
        problem (Problem): a `Problem` object

    Returns:
        pb.Problem: a `Problem` message
    """
    # Create an empty `Problem` message.
    message = pb.Problem()

    # Set the name of the problem.
    message.name = problem.name

    # Set the id of the problem.
    message.id = str(ULID())

    # Set sense of the problem.
    if problem.sense == ProblemSense.MINIMUM:
        message.sense = pb.ProblemSense.MIN
    else:
        message.sense = pb.ProblemSense.MAX

    # Set the objective function.
    message.objective = expression_to_message(problem.objective)

    # Set the constraints.
    message.constraints.extend(
        [
            constraint_to_message(constraint)
            for constraint in problem.constraints.values()
        ]
    )

    # Set the user-defined penalties.
    message.penalties.extend(
        [penalty_to_message(penalty) for penalty in problem.penalties.values()]
    )

    return message
