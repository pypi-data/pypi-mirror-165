from dataclasses import dataclass
from typing import Optional

from jijmodeling.sampleset.solving_time import SolvingTime
from jijmodeling.sampleset.system_time import SystemTime


@dataclass
class MeasuringTime:
    """Schema for measuring time.

    Attributes:
        solve (Optional[SolvingTime], optional): Instance of SolvingTime. This means solver running time. Defaults to None.
        system (Optional[SystemTime], optional): Instance of SystemTime. This means time about jijzept system. Defaults to None.
        total (Optional[float], optional): Total time from submitting problem to obtaining solution. Defaults to None.
    """

    solve: Optional[SolvingTime] = None
    system: Optional[SystemTime] = None
    total: Optional[float] = None
