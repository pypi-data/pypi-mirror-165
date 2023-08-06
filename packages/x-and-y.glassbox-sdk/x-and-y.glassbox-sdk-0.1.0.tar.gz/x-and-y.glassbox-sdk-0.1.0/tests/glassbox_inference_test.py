import unittest

from glassbox_sdk.glassbox import GlassBox, GlassBoxConfig
from glassbox_sdk.glassbox_config import ModelRef
from glassbox_sdk.glassbox_inference import GlassBoxInference, InferenceState


def random_image():
    import random
    from PIL import Image
    im = Image.new('RGB', (100, 100))
    pixels = im.load()
    for x in range(im.size[0]):
        for y in range(im.size[1]):
            pixels[x, y] = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    return im


class GlassboxTest(unittest.TestCase):

    def test(self):
        config = GlassBoxConfig(url="https://odq9ysmgu2.execute-api.eu-central-1.amazonaws.com/Beta/api/dispatch",
                                api_key="CYAYQSDVJ0EHL8M4WMW5",
                                api_secret="Z6NiFr9KtkGZM5FMRwU9NdCH5PzC4W4nzlHhcJhrvgQ")

        glassbox = GlassBox(config)

        model_ref = ModelRef("x-and-y", "opus-mt-en-de", "0.0.3", "cpu-fp16")
        inference = GlassBoxInference(model_ref, {"a": 1}, {"b": 2}, InferenceState.SUCCESS, 10)

        inference.add_xai_image(random_image())

        glassbox.create_inference(inference)

    def test_read_inferences(self):
        config = GlassBoxConfig(url="https://odq9ysmgu2.execute-api.eu-central-1.amazonaws.com/Beta/api/dispatch",
                                api_key="CYAYQSDVJ0EHL8M4WMW5",
                                api_secret="Z6NiFr9KtkGZM5FMRwU9NdCH5PzC4W4nzlHhcJhrvgQ")

        glassbox = GlassBox(config)

        model_ref = ModelRef("x-and-y", "opus-mt-en-de", "0.0.3", "cpu-fp16")
        print(glassbox.read_inferences(model_ref))

    def test_abc(self):
        config = GlassBoxConfig(url="https://odq9ysmgu2.execute-api.eu-central-1.amazonaws.com/Beta/api/dispatch",
                                api_key="CYAYQSDVJ0EHL8M4WMW5",
                                api_secret="Z6NiFr9KtkGZM5FMRwU9NdCH5PzC4W4nzlHhcJhrvgQ")

        glassbox = GlassBox(config)

        from PIL import Image

        for i in range(1, 16):
            path = "/home/christian/IdeaProjects/c7nw3r/onnx-explainer/onnx_explainer"
            inference = GlassBoxInference.from_json(f"{path}/run_{i}.json")
            inference.add_xai_image(Image.open(f"{path}/bar_{i}.png"))
            inference.add_xai_image(Image.open(f"{path}/beeswarm_{i}.png"))
            # inference.add_xai_image(Image.open(f"{path}/summary_{i}.png"))

            glassbox.create_inference(inference)