import os
from unittest import mock

import requests

path = os.path.dirname(os.path.realpath(__file__))


def request_loader(response_name: str):
    def _decorate(func):
        def loader(*args, **kwargs):
            with open(f"{path}/responses/{response_name}.json", mode="r") as f:
                data = f.readlines()
            response = requests.Response()
            response.status_code = int(response_name.split("_")[-1])
            response._content = "\n".join(data).encode("utf-8")

            with mock.patch("requests.request", return_value=response) as patched:
                kwargs["patched"] = patched
                func(*args, **kwargs)

        return loader

    return _decorate
