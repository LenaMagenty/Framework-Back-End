from pydantic import BaseModel, Field

MIN_GRADE = 0
MAX_GRADE = 5


class BaseGrade(BaseModel):
    teacher_id: int
    student_id: int
    grade: int = Field(ge=MIN_GRADE, le=MAX_GRADE)
