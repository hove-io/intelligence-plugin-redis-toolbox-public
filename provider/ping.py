from typing import Any, Union

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage


class RedisPingTool(Tool):
    @property
    def host(self) -> str:
        return self.runtime.credentials["host"]

    @property
    def port(self) -> int:
        return int(self.runtime.credentials["port"])

    @property
    def username(self) -> str:
        return self.runtime.credentials["username"]

    @property
    def password(self) -> str:
        return self.runtime.credentials["password"]

    def _invoke(
        self,
        user_id: str,
        tool_parameters: dict[str, Any],
    ) -> Union[ToolInvokeMessage, list[ToolInvokeMessage]]:
        """
        invoke tools
        """
        return self._ping()

    def _ping(self) -> Any:
        import redis

        r = redis.Redis(host=self.host, port=self.port, username=self.username, password=self.password, db=0)
        connected = r.ping()

        if connected:
            return self.create_text_message(text="OK")
        else:
            raise Exception("Could not connect to Redis")
