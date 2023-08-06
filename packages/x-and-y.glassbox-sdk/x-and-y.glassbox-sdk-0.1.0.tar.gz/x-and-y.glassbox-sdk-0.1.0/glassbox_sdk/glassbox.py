from glassbox_sdk.glassbox_config import GlassBoxConfig
from glassbox_sdk.glassbox_inference import GlassBoxInference
from glassbox_sdk.glassbox_model import GlassBoxModel, ModelRef
from glassbox_sdk.mixin.data_mixin import DataMixin
from glassbox_sdk.mixin.http_mixin import HttpMixin
from glassbox_sdk.spi.action import ModelAction


class GlassBox(HttpMixin, DataMixin):

    def __init__(self, config: GlassBoxConfig):
        self.config = config

    def create_model(self, model: GlassBoxModel):
        self.post({"__type__": "model/create", "model": model.as_dict()})
        for inference in model.inferences:
            self.create_inference(inference)

    def search_model(self):
        return self.post({"__type__": "model/search", "name": "leftshiftone"})

    def rate_model(self, model_ref: ModelRef):
        return self.post({"__type__": "model/rate", "modelRef": model_ref.to_string()})

    def create_inference(self, inference: GlassBoxInference):
        self.post({"__type__": "inference/create", "inference": inference.as_dict(), "private": True})
        for image in inference.images:
            self.post({
                "__type__": "inference/appendImage",
                "modelRef": inference.model_ref.to_string(),
                "imageRef": image.id,
                "base64": self.to_base64(image.image)
            })

    def read_inferences(self, model_ref: ModelRef):
        return self.post({"__type__": "inference/readAll", "modelRef": model_ref.to_string()})

    def create_action(self, action: ModelAction):
        self.post({"__type__": "action/create", "action": action.as_dict()})
