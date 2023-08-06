import json
import logging
from enum import Enum
from typing import List, Union, Optional, Tuple, OrderedDict

from glassbox_sdk.glassbox_config import ModelRef
from glassbox_sdk.glassbox_inference import GlassBoxInference
from glassbox_sdk.mixin.data_mixin import DataMixin
from glassbox_sdk.spi.back import BackTracing
from glassbox_sdk.spi.benchmark import BenchmarkTracing
from glassbox_sdk.spi.code import CodeTracing
from glassbox_sdk.spi.data import DataTracing
from glassbox_sdk.spi.label import Label
from glassbox_sdk.spi.license import License
from glassbox_sdk.spi.property import Property
from glassbox_sdk.spi.validation import Logging


class Purpose(Enum):
    TRAIN = "train"
    TEST = "test"
    EVALUATE = "evaluate"
    VALIDATE = "validate"


Purposes = Union[Purpose, List[Purpose]]


class GlassBoxModel(DataMixin):
    """
    A glass box model represents all necessary information about a ready to use AI model
    in order to reproduce the model results and to clearly identify the model.
    """

    license: Optional[License] = None
    checksum: Optional[str] = None
    size: Optional[str] = None
    url: Optional[str] = None

    description: Optional[str] = None
    labels: List[str] = []
    benchmarks: List[BenchmarkTracing] = []
    properties: OrderedDict = {}
    hyper_parameters: OrderedDict = {}

    back_tracing: Optional[BackTracing] = None
    data_tracing: List[Tuple[DataTracing, Purposes, Optional[Logging]]] = []
    code_tracing: List[Tuple[CodeTracing, Purposes, Optional[Logging]]] = []

    inferences: List[GlassBoxInference] = []

    def __init__(self, model_ref: ModelRef):
        self.group = model_ref.group
        self.name = model_ref.name
        self.version = model_ref.version
        self.variant = model_ref.variant

    def add_benchmark(self, benchmark: BenchmarkTracing):
        """
        Adds the given benchmark instance
        """
        self.benchmarks.append(benchmark)

    def add_benchmarks(self, benchmarks: List[BenchmarkTracing]):
        """
        Adds the given list of benchmark instances
        """
        self.benchmarks.extend(benchmarks)

    def add_properties(self, key_values: dict):
        """
        Adds the given key value pairs
        """
        self.properties.update(key_values)

    def add_property(self, key: Union[str, Property], value: any):
        """
        Adds the given key value pair
        """
        key = key.value if isinstance(key, Property) else key
        self.properties[key] = value

    def add_label(self, label: Union[Label, str]):
        """
        Adds the given label
        """
        if label not in self.labels:
            self.labels.append(label.name.lower() if isinstance(label, Label) else label)

    def add_hyper_parameter(self, key: str, value: any):
        """
        Adds the given hyper parameter
        """
        self.hyper_parameters[key] = value

    def add_hyper_parameters(self, hyper_parameters: dict):
        """
        Adds the given hyper parameters
        """
        self.hyper_parameters.update(self.to_string_dict(hyper_parameters))

    def add_code(self, code: CodeTracing, purposes: Purposes, logs: Optional[Logging] = None):
        """
        Adds the given code tracking in combination with its purpose
        """
        self.code_tracing.append((code, purposes, logs))

    def add_data(self, data: DataTracing, purposes: Purposes, logs: Optional[Logging] = None):
        """
        Adds the given data tracking in combination with itspurpose
        """
        self.data_tracing.append((data, purposes, logs))

    def add_inference(self, inference: GlassBoxInference):
        """
        Adds the given inference to the list of linked inferences
        """
        self.inferences.append(inference)

    def validate(self):
        """
        Validates the glass box model
        """
        assert self.group is not None, "group must not be None"
        assert self.name is not None, "name must not be None"
        assert self.version is not None, "version must not be None"
        assert self.checksum is not None, "checksum must not be None"
        assert self.size is not None, "size must not be None"
        assert self.url is not None, "url must not be None"
        assert self.license is not None, "license must not be None"
        assert self.description is not None, "description must not be None"
        assert len(self.labels) > 0, "labels must not be empty"
        assert len(self.benchmarks) > 0, "benchmarks must not be empty"
        assert len(self.hyper_parameters) > 0, "hyper_parameters must not be empty"
        assert len(self.data_tracing) > 0, "data_tracing must not be empty"
        assert len(self.code_tracing) > 0, "code_tracing must not be empty"
        assert self.inferences is not None, "inferences must not be None"

        if Property.SEED_VALUE.value not in self.properties:
            logging.warning("missing SEED_VALUE leads to a lower model score")

        if Property.PARAMETER_SIZE.value not in self.properties:
            logging.warning("missing PARAMETER_SIZE leads to a lower model score")

    def as_dict(self):
        """
        Returns the glass box model as a dictionary
        """
        self.validate()

        def tuple_to_dict(data: Tuple[any, Purposes, Optional[Logging]]):
            purposes = data[1] if isinstance(data[1], list) else [data[1]]
            purposes = list(map(lambda x: x.name.lower(), purposes))

            _obj = {"purposes": purposes}
            for k, v in data[0].__dict__.items():
                if v is not None:
                    _obj[k] = v
            if data[2] is not None:
                _obj["logging"] = data[2].as_dict()
            return _obj

        obj = {
            "group": self.group,
            "name": self.name,
            "version": self.version,
            "variant": self.variant,
            "license": self.license.__dict__,
            "checksum": self.checksum,
            "size": self.size,
            "url": self.url,
            "labels": self.labels,
            "benchmarks": list(map(lambda x: x.__dict__, self.benchmarks)),
            "properties": self.properties,
            "hyperParameters": self.hyper_parameters,
            "dataTracking": list(map(lambda x: tuple_to_dict(x), self.data_tracing)),
            "codeTracking": list(map(lambda x: tuple_to_dict(x), self.code_tracing)),
            "inferences": list(map(lambda x: x.id, self.inferences))
        }

        if self.back_tracing is not None:
            obj["backTracking"] = self.back_tracing.__dict__

        if self.description is not None:
            from html import escape
            obj["description"] = escape(self.description)

        return obj

    def save(self, name: str):
        """
        Saves the glassbox model as a json file.
        """
        with open(name, "w") as outfile:
            outfile.write(json.dumps(self.as_dict(), indent=4))
