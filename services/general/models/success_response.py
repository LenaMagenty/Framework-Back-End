from pydantic import BaseModel, ConfigDict


class SuccessResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")  # Запрет дополнительных полей в запросе.

    detail: str