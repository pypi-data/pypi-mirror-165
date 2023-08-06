from dataclasses import dataclass
from typing import Union

from glassbox_sdk.spi.code import CodeTracing
from glassbox_sdk.spi.traceable import Traceable


@dataclass
class ExportTracing(Traceable):
    model: CodeTracing
    exporter: CodeTracing

    def __post_init__(self):
        self.type = "export"


@dataclass
class ModelHubTracing(Traceable):
    url: str

    def __post_init__(self):
        self.type = "modelHub"


BackTracing = Union[ExportTracing, ModelHubTracing]
