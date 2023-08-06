import base64
import hmac
import json

import requests

from glassbox_sdk.glassbox_config import GlassBoxConfig


class HttpMixin:
    config: GlassBoxConfig

    def hmac(self, key: str, message: str):
        _hmac = hmac.new(key=key.encode(), digestmod="sha256")
        _hmac.update(bytes(message, encoding="utf-8"))
        return base64.b64encode(_hmac.digest()).decode()

    # noinspection PyMethodMayBeStatic
    def to_json(self, obj: dict):
        return json.dumps(obj, separators=(",", ":"))

    def post(self, data: {}):
        message = self.to_json(data)

        print("hmac")
        print(self.hmac(self.config.api_secret, message))
        print(message)

        headers = {
            "Content-Type": "application/json",
            "Authorization": "HMAC " + self.config.api_key + ":" + self.hmac(self.config.api_secret, message)
        }
        response = json.loads(requests.post(self.config.url, data=message, headers=headers).text)
        if response is not None and "errorMessage" in response:
            raise ValueError(response["errorMessage"])

        return response
