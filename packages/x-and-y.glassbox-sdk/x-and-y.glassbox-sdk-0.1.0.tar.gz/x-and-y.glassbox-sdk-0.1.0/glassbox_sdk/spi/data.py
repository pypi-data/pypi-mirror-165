from dataclasses import dataclass
from typing import Optional

from glassbox_sdk.spi.traceable import Traceable


class DataTracing(Traceable):
    pass


@dataclass
class Dataset(DataTracing):
    """
    A data instance represents a collection of information used by an ai model for training or testing.
    """

    url: str
    checksum: Optional[str] = None

    def __post_init__(self):
        self.type = "dataset"
