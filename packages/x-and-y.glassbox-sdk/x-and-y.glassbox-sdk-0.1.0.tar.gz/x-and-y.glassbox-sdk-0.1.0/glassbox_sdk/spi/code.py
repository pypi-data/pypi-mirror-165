from dataclasses import dataclass

from glassbox_sdk.spi.traceable import Traceable


class CodeTracing(Traceable):
    pass


@dataclass
class GitCommit(CodeTracing):
    """
    A Git instance represents a code repository state at a custom hash value.
    """

    url: str
    hash: str

    def __post_init__(self):
        self.type = "commit"


@dataclass
class GitTag(CodeTracing):
    """
    A Git instance represents a code repository state at a custom git tag.
    """

    url: str
    tag: str

    def __post_init__(self):
        self.type = "tag"
