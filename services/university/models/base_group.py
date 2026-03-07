from pydantic import BaseModel, ConfigDict


class BaseGroup(BaseModel):
    model_config = ConfigDict(extra="forbid")  # Запрет дополнительных полей в запросе.

    name: str

