from typing import Literal

from pydantic import BaseModel, ConfigDict


class LoginResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")  # Запрет дополнительных полей в запросе.

    access_token: str
    token_type: Literal["Bearer"]
