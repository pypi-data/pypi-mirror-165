from dataclasses import dataclass

from glassbox_sdk.spi.traceable import Traceable


@dataclass
class BenchmarkTracing(Traceable):
    url: str


@dataclass
class Bleu(BenchmarkTracing):
    """
    A benchmark specified by https://aclanthology.org/P02-1040.pdf
    """

    score: str

    def __post_init__(self):
        self.type = "bleu"


@dataclass
class ChrF(BenchmarkTracing):
    """
    A benchmark specified by https://aclanthology.org/W15-3049.pdf
    """

    score: str

    def __post_init__(self):
        self.type = "chrf"


@dataclass
class MeanSquaredError(BenchmarkTracing):
    score: str

    def __post_init__(self):
        self.type = "mse"


@dataclass
class MeanAbsoluteError(BenchmarkTracing):
    score: str

    def __post_init__(self):
        self.type = "mae"


@dataclass
class R2Score(BenchmarkTracing):
    score: str

    def __post_init__(self):
        self.type = "r2"


@dataclass
class ExplainedVarianceScore(BenchmarkTracing):
    score: str

    def __post_init__(self):
        self.type = "ev"


@dataclass
class MeanPinballLoss(BenchmarkTracing):
    score: str

    def __post_init__(self):
        self.type = "mpl"


@dataclass
class D2PinballScore(BenchmarkTracing):
    score: str

    def __post_init__(self):
        self.type = "d2p"

@dataclass
class D2AbsoluteErrorScore(BenchmarkTracing):
    score: str

    def __post_init__(self):
        self.type = "d2ae"


@dataclass
class CustomBenchmark(BenchmarkTracing):
    """
    A custom benchmark implementation.
    """
    type: str
    score: str
