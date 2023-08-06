import json
from html import unescape
from typing import Tuple

from glassbox_sdk.glassbox_model import GlassBoxModel, ModelRef, Purposes, Purpose
from glassbox_sdk.spi.back import ModelHubTracing
from glassbox_sdk.spi.benchmark import Bleu, ChrF
from glassbox_sdk.spi.code import GitCommit, CodeTracing
from glassbox_sdk.spi.data import Dataset, DataTracing
from glassbox_sdk.spi.license import License


def create_model(path: str):
    with open(path, 'r') as openfile:
        obj = json.load(openfile)

    model = GlassBoxModel(ModelRef(obj["group"], obj["name"], obj["version"], obj["variant"]))
    model.checksum = obj["checksum"]
    model.license = License(obj["license"]["name"], obj["license"]["url"])
    model.size = obj["size"]
    model.url = obj["url"]
    model.description = unescape(obj["description"])
    model.labels = obj["labels"]
    model.benchmarks = list(map(_to_benchmark, obj["benchmarks"]))
    model.properties = obj["properties"]
    model.hyper_parameters = obj["hyperParameters"]
    model.data_tracing = list(map(_to_data_tracing, obj["dataTracking"]))
    model.code_tracing = list(map(_to_code_tracing, obj["codeTracking"]))
    model.back_tracing = _to_back_tracing(get(obj, "backTracking"))

    return model


def _to_benchmark(data: {}):
    """
    Deserializes the given data to a Benchmark instance.
    :param data: the data to deserialize
    :return: Benchmark
    """
    if data["type"] == "bleu":
        return Bleu(data["url"], data["score"])
    if data["type"] == "chrf":
        return ChrF(data["url"], data["score"])
    raise ValueError("cannot deserialize benchmark " + data.type)


def get(data: {}, key: str):
    return data[key] if key in data else None


def _to_data_tracing(data: {}) -> Tuple[DataTracing, Purposes]:
    """
    Deserializes the given data to a DataTracing instance.
    :param data: the data to deserialize
    :return: Tuple[DataTracing, Purposes]
    """
    if data["type"] == "dataset":
        return Dataset(data["url"], get(data, "checksum")), list(map(_to_purpose, data["purposes"]))
    raise ValueError("cannot deserialize data tracing " + data.type)


def _to_code_tracing(data: {}) -> Tuple[CodeTracing, Purposes]:
    """
    Deserializes the given data to a CodeTracing instance.
    :param data: the data to deserialize
    :return: Tuple[CodeTracing, Purposes]
    """
    if data["type"] == "commit":
        return GitCommit(data["url"], data["hash"]), list(map(_to_purpose, data["purposes"]))
    raise ValueError("cannot deserialize data tracing " + data.type)


def _to_back_tracing(data: {}):
    """
    Deserializes the given data to a back tracing instance.
    :param data: the data to deserialize
    :return: BackTracing
    """
    if data is None:
        return None

    if data["type"] == "modelHub":
        return ModelHubTracing(data["url"])
    raise ValueError("cannot deserialize back tracing " + data.type)


def _to_purpose(text: str):
    """
    Deserializes the given text to a Purpose instance.
    :param text: the text to deserialize
    :return: Purpose
    """

    if text == "train":
        return Purpose.TRAIN
    if text == "test":
        return Purpose.TEST
    if text == "evaluate":
        return Purpose.EVALUATE
    if text == "validate":
        return Purpose.VALIDATE
    raise ValueError("cannot deserialize purpose " + text)
