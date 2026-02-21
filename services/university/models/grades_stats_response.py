from pydantic import BaseModel, ConfigDict


class GradesStatsResponse(BaseModel):
    model_config = ConfigDict(extra='forbid')

    count: int
    min: int
    max: int
    avg: float