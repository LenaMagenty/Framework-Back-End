from enum import StrEnum

from pydantic import BaseModel, ConfigDict, EmailStr


class DegreeEnum(StrEnum):
    ASSOCIATE = "Associate"
    BACHELOR = "Bachelor"
    MASTER = "Master"
    DOCTORATE = "Doctorate"


class BaseStudent(BaseModel):
    model_config = ConfigDict(extra="forbid")  # Запрет дополнительных полей в запросе.

    first_name: str
    last_name: str
    email: EmailStr
    degree: DegreeEnum
    phone: str  # Желательно посмотреть валидацию именно в требованиях. Разработчик мог ошибиться в Swagger.
    group_id: int
