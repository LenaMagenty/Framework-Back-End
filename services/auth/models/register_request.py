from pydantic import BaseModel, ConfigDict, EmailStr


class RegisterRequest(BaseModel):
    model_config = ConfigDict(extra="forbid") # Запрет дополнительных полей в запросе.

    username: str
    password: str
    password_repeat: str
    email: EmailStr