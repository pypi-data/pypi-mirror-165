from dataclasses import dataclass
from typing import Optional


@dataclass
class SolvingTime:
    """Schema for solver running time.

    Attributes:
        preprocess (Optional[float], optional): Time to preprocess. Defaults to None.
        solve (Optional[float], optional): Time to solve. Defaults to None.
        postprocess (Optional[float], optional): Time to postprocess. Defaults to None.
    """

    preprocess: Optional[float] = None
    solve: Optional[float] = None
    postprocess: Optional[float] = None
