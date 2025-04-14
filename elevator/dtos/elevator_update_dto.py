from typing import Optional
from pydantic import BaseModel, ConfigDict

class ElevatorUpdateDto(BaseModel):
    current_floor: Optional[int]
    direction: Optional[str]
    is_open: Optional[bool]
    target_floors: Optional[set[int]]
    is_moving: Optional[bool]

    model_config = ConfigDict(validate_default=True, extra="ignore")

    def dict(self):
        return self.__dict__