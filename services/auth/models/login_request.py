from pydantic import BaseModel, ConfigDict


class LoginRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")  # Запрет дополнительных полей в запросе.

    username: str
    password: str