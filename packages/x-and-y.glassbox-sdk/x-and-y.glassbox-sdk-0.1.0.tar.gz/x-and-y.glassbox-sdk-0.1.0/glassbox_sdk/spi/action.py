from dataclasses import dataclass


@dataclass
class ModelAction:
    group: str
    name: str
    webhook: str

    def as_dict(self):
        return {
            "group": self.group,
            "name": self.name,
            "webhook": self.webhook
        }
