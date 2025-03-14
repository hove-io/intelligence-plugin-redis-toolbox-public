from typing import Any, Union

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage


class RedisWorkflowVarsTool(Tool):
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
        import redis

        r = redis.Redis(host=self.host, port=self.port, username=self.username, password=self.password, db=0)

        app_id = tool_parameters["app_id"]
        keys_raw = tool_parameters["keys"]
        values_raw = tool_parameters.get("values")
        _delete = tool_parameters.get("delete", "False")
        if _delete == "True":
            delete_keys = True
        elif _delete == "False":
            delete_keys = False
        else:
            raise ValueError(f"Invalid value for delete: {_delete}")

        keys = keys_raw.split(",")
        values = values_raw.split(",") if values_raw else []

        if values_raw:
            data = dict(zip(keys, values))
            pipeline = r.pipeline()
            for key, value in data.items():
                pipeline.set(f"workflow_vars:{app_id}:{key}", value)
            pipeline.execute()

            return self.create_json_message(object={"app_id": app_id, **data})
        else:
            out_dict = {"app_id": app_id}
            for key in keys:
                if delete_keys:
                    r.delete(f"workflow_vars:{app_id}:{key}")
                else:
                    value = r.get(f"workflow_vars:{app_id}:{key}")
                    if value:
                        value = value.decode("utf-8")
                    out_dict[key] = value
            return self.create_json_message(object=out_dict)
