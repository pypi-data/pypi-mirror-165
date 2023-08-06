import json
from os.path import isfile

from glassbox_sdk.glassbox_model import GlassBoxModel, ModelRef
from glassbox_sdk.spi.back import ModelHubTracing
from glassbox_sdk.spi.license import CC_BY_4


def read_lines(path: str):
    with open(path, 'r') as openfile:
        return openfile.readlines()


def read_json(path: str):
    with open(path, 'r') as openfile:
        return json.load(openfile)


def create_model_from_xy(path: str):
    # info.json
    # *********************************
    config = read_json(path + "/info.json")
    group = config["group"]
    name = config["name"]
    version = config["version"]
    variant = config["optimization"] + "-" + config["quantization"]

    model = GlassBoxModel(ModelRef(group, name, version, variant))
    model.url = "https://x-and-y.ai/model/" + group + "/" + name + "/" + version + "/" + variant
    model.license = _to_license(config["license"])
    model.size = config["size"]
    model.labels = config["labels"]
    # TODO: add parameter size and graph node count
    model.add_property("format", config["format"])
    model.add_property("opsetVersion", config["opsetVersion"])
    model.add_property("exporterVersion", config["exporterVersion"])
    model.add_property("libraries", config["libraries"])
    model.add_property("python", config["python"])
    model.back_tracing = ModelHubTracing(config["baseModel"]["url"] + config["baseModel"]["name"])

    # TODO: add tags
    # TODO: add back tracking

    # checksum
    # **********************************
    model.checksum = read_lines(path + "/checksum")[0]

    # config.json
    # **********************************
    model.hyper_parameters = read_json(path + "/config.json")

    # readme.md
    # **********************************
    model.description = ""

    if isfile(path + "/readme.md"):
        model.description += "\n".join(read_lines(path + "/readme.md"))

        if isfile(path + "/changelog.md"):
            model.description += "\n\n"
            model.description += "\n".join(read_lines(path + "/changelog.md"))

    return model


def _to_license(name: str):
    if name == "cc-by-4.0":
        return CC_BY_4
    raise ValueError("cannot deserialize " + name)
