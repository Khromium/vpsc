"""リクエストモジュール

APIへのリクエストを直接的に行なっているモジュールです。
ページングなどの処理もこちらで対応。

"""
import json
from collections.abc import Sized, Iterator
from types import MappingProxyType
from typing import Literal, Optional, Type, TYPE_CHECKING

import requests
from pydantic import BaseModel

if TYPE_CHECKING:
    from client import APIConfig


class APIRequest(Iterator, Sized):
    unsafe_methods = ["post", "put", "delete"]
    generator = None
    count = 0

    def __init__(self, config: "APIConfig", header: MappingProxyType):
        self.config = config
        self.headers = dict(header)
        self.headers["Authorization"] = f"Bearer {self.config.api_key}"

    def __len__(self):
        if self.count is None:
            raise ValueError("request first")

        return self.count

    def __iter__(self):
        if self.generator is None:
            raise NotImplementedError()
        return self

    def __next__(self):
        if self.generator is None:
            raise NotImplementedError()
        return next(self.generator)

    def __generator(self, prefetch_data: list, response_obj: Optional[Type[BaseModel]], per_page: int, **request_args):
        for item in prefetch_data:
            yield response_obj(**item)
        for i in range(2, per_page, self.count):  # 2ページ目から取得
            request_args["params"] = {"per_page": per_page, "page": i}
            next_url = request_args["url"]
            while next_url:
                request_args["url"] = next_url
                results = self._fetch(**request_args)
                for item in results["results"]:
                    yield response_obj(**item)
                next_url = results.get("next", False)

    def request(
        self,
        endpoint: str,
        method: Literal["get", "post", "put", "delete"],
        data: Optional[BaseModel] = None,
        response_obj: Optional[Type[BaseModel]] = None,
    ):
        content = None
        if method in self.unsafe_methods:
            self.headers["content-type"] = "application/json"
            if data:
                content = data.model_dump_json(exclude_unset=True).encode("utf-8")

        req_data = {
            "method": method,
            "url": f"{self.config.host}{endpoint}",
            "headers": self.headers,
        }
        if content:
            req_data["data"] = content

        result = self._fetch(**req_data)
        if result is None:
            return None

        if self.count > 0 and result.get("results", False):
            req_data["url"] = result.get("next", False)
            self.generator = self.__generator(
                prefetch_data=result["results"], response_obj=response_obj, per_page=10, **req_data
            )
            return self
        else:
            return response_obj(**result)

    def _fetch(self, **req_data) -> Optional[dict]:
        res = requests.request(**req_data)
        res.raise_for_status()
        if res.content is not None and len(res.content) > 3:
            data = res.json()
            self.count = data.get("count", 1)
            return data
        return None
