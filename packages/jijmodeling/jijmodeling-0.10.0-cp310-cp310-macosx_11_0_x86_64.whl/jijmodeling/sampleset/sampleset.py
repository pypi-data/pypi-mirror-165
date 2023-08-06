from copy import deepcopy
from dataclasses import asdict, dataclass
from typing import Dict, List

import pandas as pd

from jijmodeling.exceptions import SerializeSampleSetError
from jijmodeling.sampleset.evaluation import Evaluation
from jijmodeling.sampleset.measuring_time import MeasuringTime
from jijmodeling.sampleset.record import Record


@dataclass
class SampleSet:
    """Schema for sampleset.

    Attributes:
        record (Record): Record object. This means basic infomation of solutions.
        evaluation (Evaluation): Evaluation object. This means evaluation results of solutions.
        measuring_time (MeasuringTime): MeasuringTime object. This means measuring time of various processing until solutions is obtained.
    """

    record: Record
    evaluation: Evaluation
    measuring_time: MeasuringTime

    def to_pandas_dataframe(self, dense: bool = False):
        record = self.record.to_pandas_dataframe(dense=dense)
        evaluation = self.evaluation.to_pandas_dataframe()

        return pd.concat([record, evaluation], axis=1)

    def to_dense(self, inplace: bool = False):
        if inplace:
            self.record.to_dense(inplace=inplace)
            return self
        else:
            record = self.record.to_dense(inplace=inplace)
            return SampleSet(
                record=record,
                evaluation=self.evaluation,
                measuring_time=self.measuring_time,
            )

    @classmethod
    def from_serializable(cls, obj: Dict):
        """To Instance of SampleSet from Dict of SampleSet.

        Args:
            obj (Dict): Dict of SampleSet.

        Returns:
            SampleSet: SampleSet obj.
        """
        for key in ["record", "evaluation", "measuring_time"]:
            if key not in obj.keys():
                raise SerializeSampleSetError(f'"obj" does not contain "{key}" key')

        solution = {}
        for k, v in obj["record"]["solution"].items():
            solution[k] = [(tuple(vi[0]), vi[1], tuple(vi[2])) for vi in v]
        obj["record"]["solution"] = solution

        record = Record(**obj["record"])
        evaluation = Evaluation.from_serializable(obj["evaluation"])
        measuring_time = MeasuringTime(**obj["measuring_time"])

        return cls(
            record=record,
            evaluation=evaluation,
            measuring_time=measuring_time,
        )

    def to_serializable(self):
        evaluation_to_serializable_obj = self.evaluation.to_serializable()
        to_serializable_obj = asdict(self)
        to_serializable_obj["evaluation"] = evaluation_to_serializable_obj
        return to_serializable_obj

    def _extend(self, other):
        self.record._extend(other.record)
        self.evaluation._extend(other.evaluation)
        # TODO: concatenates MeasuringTime objects


def concatenate(
    jm_sampleset_list: List[SampleSet],
) -> SampleSet:
    """
    Concatenates SampleSet objects into a single SampleSet object.

    Args:
        jm_sampleset_list (List[SampleSet]): a list of SampleSet objects

    Returns:
        SampleSet: a SampleSet object that be concatenated
    """
    if len(jm_sampleset_list) == 0:
        raise ValueError("empty list is invalid")
    elif len(jm_sampleset_list) == 1:
        return jm_sampleset_list[0]
    else:
        concat_sampleset = deepcopy(jm_sampleset_list[0])
        for jm_sampleset in jm_sampleset_list[1:]:
            concat_sampleset._extend(jm_sampleset)
        return concat_sampleset
