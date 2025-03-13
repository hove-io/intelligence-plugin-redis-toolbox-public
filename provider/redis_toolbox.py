from typing import Any

from dify_plugin import ToolProvider
from dify_plugin.errors.tool import ToolProviderCredentialValidationError

from .ping import RedisPingTool


class RedisToolsProvider(ToolProvider):
    def _validate_credentials(self, credentials: dict[str, Any]) -> None:
        try:
            RedisPingTool().from_credentials(credentials).invoke(
                tool_parameters={},
            )
        except Exception as e:
            raise ToolProviderCredentialValidationError(str(e)) from e
