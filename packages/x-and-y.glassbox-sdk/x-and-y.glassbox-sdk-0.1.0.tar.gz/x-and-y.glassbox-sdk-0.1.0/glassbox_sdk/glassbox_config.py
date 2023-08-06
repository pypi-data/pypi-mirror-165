import re
from dataclasses import dataclass
from typing import Optional


@dataclass
class GlassBoxConfig:
    """
    The config class is used to establish a connection to the glassbox backend.
    """

    url: str
    api_key: str
    api_secret: str

@dataclass
class ModelRef:
    """
    A model ref object is used to uniquely identify an AI model.
    """
    group: str
    name: str
    version: str
    variant: Optional[str] = None

    @property
    def is_snapshot(self):
        """
        Indicates if the model ref points to a snapshot version.
        A snapshot version model spec is mutable.
        :return: bool
        """
        return self.version.endswith("-SNAPSHOT")

    @staticmethod
    def from_string(model_ref: str) -> 'ModelRef':
        parsed = re.search(r"([a-zA-Z0-9_-]+)\:([a-zA-Z0-9_-]+)\:([0-9]+\.[0-9]+\.[0-9]+)(@[a-zA-Z0-9_-]+)?", model_ref)

        group = parsed.group(1)
        name = parsed.group(2)
        version = parsed.group(3)
        variant = parsed.group(4)[1:] if parsed.group(4) is not None else None
        return ModelRef(group, name, version, variant)

    def to_string(self):
        if self.variant is not None:
            return f"{self.group}:{self.name}:{self.version}@{self.variant}"
        return f"{self.group}:{self.name}:{self.version}"

    def as_dict(self):
        return {
            "group": self.group,
            "name": self.name,
            "version": self.version,
            "variant": self.variant
        }

    @staticmethod
    def from_dict(data: dict):
        return ModelRef(data["group"], data["name"], data["version"],data["variant"])