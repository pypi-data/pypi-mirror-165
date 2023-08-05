import abc
import collections
import os
from itertools import compress
from typing import List, TYPE_CHECKING, Union

from .proxy_info import ProxyInfo
from ..._core.session import SessionType

if TYPE_CHECKING:
    from ..._core.session import Session

StreamServiceInfo = collections.namedtuple(
    "StreamServiceInfo",
    ["scheme", "host", "port", "path", "data_formats", "location", "transport"],
)


class StreamCxnConfig(abc.ABC):
    def __init__(
        self,
        infos: Union[List["StreamServiceInfo"], "StreamServiceInfo"],
        protocols: Union[List[str], str],
        transport: str = "websocket",
    ):
        if isinstance(infos, list) and len(infos) == 0:
            raise ValueError("infos are empty")

        if not isinstance(infos, list):
            infos = [infos]

        if not isinstance(protocols, list):
            protocols = [protocols]

        self._num_infos = len(infos)
        self._infos = infos
        self._protocols = protocols
        self._transport = transport
        self._available = [True] * len(infos)
        self._index = 0

    @property
    def transport(self):
        return self._transport

    @property
    def info(self):
        return self._infos[self._index]

    @property
    def num_infos(self) -> int:
        return self._num_infos

    def info_not_available(self) -> None:
        self._available[self._index] = False

    def has_available_info(self) -> bool:
        return any(self._available)

    def next_available_info(self) -> int:
        if not self.has_available_info():
            raise ValueError("No available infos")
        infos = compress(
            self._infos[self._index + 1 :] + self._infos[: self._index],
            self._available[self._index + 1 :] + self._available[: self._index],
        )
        info = next(infos)
        self._index = self._infos.index(info)
        if self._index == 0:
            raise StopIteration()
        return self._index

    @property
    def url(self):
        return self._get_url(self.info)

    @property
    def url_scheme(self):
        return self.info.scheme

    @property
    def urls(self):
        return [self._get_url(info) for info in self._infos]

    @property
    def headers(self):
        return []

    @property
    def data_formats(self):
        return self.info.data_formats

    @property
    def supported_protocols(self):
        return self._protocols

    def reset_reconnection_config(self):
        self._index = 0

    @property
    def no_proxy(self):
        return ProxyInfo.get_no_proxy()

    @property
    def proxy_config(self):
        proxies_info = ProxyInfo.get_proxies_info()
        if self.url_scheme == "wss":
            # try to get https proxy then http proxy if https not configured
            return proxies_info.get("https", proxies_info.get("http", None))
        else:
            return proxies_info.get("http", None)

    @property
    def data_fmt(self):
        if not self.data_formats:
            return ""
        return self.data_formats[0]

    @abc.abstractmethod
    def _get_url(self, info: "StreamServiceInfo") -> str:
        pass

    def __str__(self) -> str:
        urls = "\n\t\t\t   ".join(self.urls)
        s = (
            f"{self.__class__.__name__}\n"
            f"\t\theaders={self.headers},data_formats={self.data_formats},supported_protocols={self.supported_protocols},no_proxy={self.no_proxy},proxy_config={self.proxy_config},data_fmt={self.data_fmt}\n"
            f"\t\turls : {urls}"
        )
        return s


class DesktopStreamCxnConfig(StreamCxnConfig):
    def __init__(
        self,
        session: "Session",
        infos: Union[List["StreamServiceInfo"], "StreamServiceInfo"],
        protocols: Union[List[str], str],
    ):
        super().__init__(infos, protocols)
        self._session = session

    @property
    def headers(self):
        app_version = os.getenv("DP_PROXY_APP_VERSION")
        headers = [f"x-tr-applicationid: {self._session.app_key}"]

        if self._session._access_token:
            headers.append(f"Authorization: Bearer {self._session._access_token}")

        if app_version and self._session.type == SessionType.DESKTOP:
            headers.append(f"app-version: {app_version}")

        return headers

    def _get_url(self, info: "StreamServiceInfo") -> str:
        return f"{info.scheme}://{info.host}:{info.port}/{info.path}"


class PlatformStreamCxnConfig(StreamCxnConfig):
    def _get_url(self, info: "StreamServiceInfo") -> str:
        if self.transport == "tcp":
            return f"{info.host}:{info.port}"
        else:
            path = info.path or "WebSocket"
            return f"{info.scheme}://{info.host}:{info.port}/{path}"


class NullStreamCxnConfig(StreamCxnConfig):
    def __init__(self):
        StreamCxnConfig.__init__(
            self, [StreamServiceInfo("", "", "", "", "", "", "")], []
        )

    def _get_url(self, info):
        return ""
