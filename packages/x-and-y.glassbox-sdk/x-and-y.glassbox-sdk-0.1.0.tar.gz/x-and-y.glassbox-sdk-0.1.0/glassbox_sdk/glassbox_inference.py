import cuid
import json
from dataclasses import dataclass
from enum import Enum
from typing import List, Union, Optional
from uuid import uuid4

from PIL import Image

from glassbox_sdk.glassbox_config import ModelRef
from glassbox_sdk.mixin.data_mixin import DataMixin

Purpose = Union[str, List[str]]


class InferenceState(Enum):
    SUCCESS = "success"
    FAILURE = "failure"


@dataclass
class GlassBoxInference:
    model_ref: ModelRef  # the reference to the model which handled the inference
    request: dict  # the request body
    response: dict  # the response body
    status: InferenceState = "success"  # the state of the inference
    duration: Optional[int] = None  # the duration of the inference

    def __post_init__(self):
        self.id = cuid.cuid()
        self.images: List[XAIImage] = []

    def add_xai_image(self, image: Image):
        # TODO: scale image
        self.images.append(XAIImage(str(uuid4()), image))

    def validate(self):
        assert self.model_ref is not None, "model ref must not be None"
        assert self.request is not None, "request body must not be None"
        assert self.response is not None, "response body must not be None"
        assert self.status is not None, "inference state must not be None"

    def as_dict(self):
        self.validate()

        return {
            "id": self.id,
            "group": self.model_ref.group,
            "name": self.model_ref.name,
            "version": self.model_ref.version,
            "variant": self.model_ref.variant,
            "request": self.request,
            "response": self.response,
            "status": self.status.value,
            "duration": self.duration,
            "images": list(map(lambda x: x.id, self.images))
        }

    def save(self, name: str):
        """
        Saves the glassbox model as a json file.
        """
        with open(name, "w") as outfile:
            outfile.write(json.dumps(self.as_dict(), indent=4))

    @staticmethod
    def from_json(path: str):
        with open(path, "r") as file:
            import json
            data = json.load(file)
            print(data)
            model_ref = ModelRef.from_dict(data["model_ref"])

        mixin = DataMixin()
        inference = GlassBoxInference(model_ref,
                                      mixin.to_string_dict(data["request"]),
                                      mixin.to_string_dict(data["response"]),
                                      InferenceState.SUCCESS,
                                      data["duration"])

        # from pathlib import Path
        # Image.open(str(Path(path).parent.absolute()) + "/bar_1.png")

        return inference


@dataclass
class XAIImage:
    id: str
    image: Image
