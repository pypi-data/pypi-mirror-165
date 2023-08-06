from dataclasses import asdict, dataclass
from typing import Dict, List, Optional, Union

import numpy as np
import pandas as pd


@dataclass
class Evaluation:
    """Schema for results of evaluating solutions.

    Attributes
        energy (List[float]): a list of values of energy.
        objective (Optional[List[float]], optional): a list of values of objective function. Defaults to None.
        constraint_violations (Optional[Dict[str, List[float]]], optional): a list of constraint violations. A key is the name of a constraint. A value is cost of a constraint. Defaults to None.
        penalty (Optional[List[Union[Dict, Dict[str, float]]]], optional): a list of costs of penalty terms. A key is the name of a penalty. A value is cost of a penalty term. Defaults to None.
    """

    energy: List[float]
    objective: Optional[List[float]] = None
    constraint_violations: Optional[Dict[str, List[float]]] = None
    penalty: Optional[List[Union[Dict, Dict[str, float]]]] = None

    def to_pandas_dataframe(self):
        evaluation = {}
        for k, v in asdict(self).items():
            if "constraint" in k:
                if v is None:
                    evaluation[k] = np.nan
                else:
                    for kc, kv in v.items():
                        evaluation[f"{k}[{kc}]"] = kv
            else:
                if v is None:
                    v = np.nan
                evaluation[k] = v
        return pd.DataFrame(evaluation)

    @classmethod
    def from_serializable(cls, obj: dict):
        return cls(
            energy=obj.get("energy"),
            objective=obj.get("objective"),
            constraint_violations=obj.get("constraint_violations"),
            penalty=obj.get("penalty"),
        )

    def to_serializable(self):
        return asdict(self)

    def _extend(self, other):
        # Concatenate energy
        self.energy.extend(other.energy)

        # Concatenate objective
        if isinstance(other.objective, list):
            self.objective.extend(other.objective)

        # Concatenate constraint_violations
        if isinstance(other.constraint_violations, dict):
            for (
                con_label,
                constraint_violation,
            ) in other.constraint_violations.items():
                self.constraint_violations[con_label].extend(constraint_violation)

        # Concatenate penalty
        if isinstance(other.penalty, list):
            self.penalty.extend(other.penalty)
