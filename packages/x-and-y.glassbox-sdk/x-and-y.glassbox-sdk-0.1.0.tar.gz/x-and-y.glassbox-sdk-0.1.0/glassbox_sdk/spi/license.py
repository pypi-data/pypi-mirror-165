from dataclasses import dataclass


@dataclass
class License:
    name: str
    url: str


CC_BY_4 = License("cc-by-4.0", "https://creativecommons.org/licenses/by/4.0/")
APACHE_2 = License("apache-2.0", "http://www.apache.org/licenses/LICENSE-2.0")
