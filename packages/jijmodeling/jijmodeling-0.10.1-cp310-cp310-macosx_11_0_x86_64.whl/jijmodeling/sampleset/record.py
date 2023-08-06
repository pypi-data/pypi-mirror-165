from dataclasses import dataclass
from typing import Dict, List, Union

import numpy as np
import pandas as pd

from jijmodeling.exceptions import SerializeSampleSetError
from jijmodeling.type_annotations import DenseSolution, SparseSolution


@dataclass
class Record:
    """Represents the Schema for solutions obtained by a solver.

    Attributes:
        solution (Dict[str, Union[List[SparseSolution], List[DenseSolution]]]): Solution. A key is the label of a decision variable. There are two type in value:
            - SparseSolution is tuple of length 3, where each element means (nonzero index, nonzero value, shpae) for solution.
            - DenseSolution is numpy.ndarray which dimension is shape of decision variable.
        num_occurrences (List[int]): Number of occurrences for each sample.
    """

    solution: Dict[str, Union[List[SparseSolution], List[DenseSolution]]]
    num_occurrences: List[int]

    def __post_init__(self):
        self._is_dense = False

    @property
    def is_dense(self) -> bool:
        """SparseSolution or DenseSolution:
            - If True, DenseSolution,
            - Else, SparseSolution.

        Returns:
            bool: True or False.
        """
        return self._is_dense

    @is_dense.setter
    def is_dense(self, b: bool):
        self._is_dense = b

    @classmethod
    def from_serializable(cls, obj: Dict):
        """To Record object from Dict of SampleSet.

        Args:
            obj (Dict): Dict of Record.

        Returns:
            Record: Record obj.
        """

        for key in ["solution", "num_occurrences"]:
            if key not in obj.keys():
                raise SerializeSampleSetError(f'"obj" does not contain "{key}" key')
        return cls(**obj)

    def to_pandas_dataframe(self) -> pd.DataFrame:
        """Convert Record object to pandas.DataFrame object.

        Returns:
            pandas.DataFrame: pandas.DataFrame object.
        """
        solution = pd.DataFrame({f"solution[{k}]": v for k, v in self.solution.items()})
        num_occurrences = pd.DataFrame({"num_occurrences": self.num_occurrences})
        return pd.concat([solution, num_occurrences], axis=1)

    def to_dense(self, inplace: bool = False):
        solution = {}
        for label, si in self.solution.items():
            array_list = []
            for nonzero_index, values, shape in si:
                array = np.zeros(shape, dtype=int)
                if array.ndim:
                    array[nonzero_index] = values
                else:
                    array = np.array(values)
                array_list.append(array)
            solution[label] = array_list
        if inplace:
            self.solution = solution
            self._solution_type = DenseSolution
        return Record(solution=solution, num_occurrences=self.num_occurrences)

    def _extend(self, other):
        for var_label, solution in other.solution.items():
            self.solution[var_label].extend(solution)
        self.num_occurrences.extend(other.num_occurrences)
