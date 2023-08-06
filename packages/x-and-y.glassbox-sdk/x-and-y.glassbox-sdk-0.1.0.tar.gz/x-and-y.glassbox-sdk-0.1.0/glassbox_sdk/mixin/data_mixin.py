from io import BytesIO

from PIL.Image import Image


class DataMixin:

    def to_string_dict(self, data: {}):
        for key in data:
            value = data[key]
            if value is None:
                continue
            elif isinstance(value, float):
                data[key] = str(data[key])
            elif isinstance(value, int):
                data[key] = str(data[key])
            elif isinstance(value, dict):
                data[key] = self.to_string_dict(value)
            elif isinstance(value, list):
                data[key] = list(map(lambda x: self.to_string_dict(x) if isinstance(x, dict) else x, value))
            else:
                data[key] = data[key]

        return data

    def to_base64(self, image: Image):
        import base64

        buff = BytesIO()
        image.save(buff, format=image.format)
        return base64.b64encode(buff.getvalue()).decode("utf-8")

    def checksum(self, data) -> str:
        import hashlib
        import pickle
        return hashlib.md5(pickle.dumps(data)).hexdigest()
