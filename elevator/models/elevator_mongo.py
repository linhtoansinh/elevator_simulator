from ..enums.directions import Direction
from pydantic import BaseModel, ConfigDict

class Elevator(BaseModel):
    elevator_id: int
    current_floor: int = 1
    direction: str | None = None
    is_open: bool = False
    target_floors: list[int] = []
    is_moving: bool = False

    model_config = ConfigDict(validate_default=True)

    def add_floors(self, floors:list[int]=[]):
        for floor in floors:
            if (floor not in self.target_floors):
                self.target_floors.append(floor)

        self.target_floors.sort()

    def remove_floor(self, floor: int):
        if floor in self.target_floors:
            self.target_floors.remove(floor)

    def set_target_floors(self, floors:list[int]=[]):
        self.target_floors = floors

    def open_door(self):
        if not self.is_moving:
                self.is_open = True

    def close_door(self):
        self.is_open = False

    def move(self):
        if len(self.target_floors) < 1:
            self.direction = None
            self.is_moving = False
            return
        
        if self.is_open:
            return

        self.is_moving = True

        if self.direction == Direction.UP.value and self.current_floor < max(self.target_floors):
            self.current_floor += 1
        elif self.direction == Direction.DOWN.value and self.current_floor > min(self.target_floors):
            self.current_floor -= 1

        if self.has_reached_top() and len(self.target_floors) > 1:
            self.direction = Direction.DOWN.value

        if self.has_reached_bottom() and len(self.target_floors) > 1:
            self.direction = Direction.UP.value

        if self.current_floor in self.target_floors:
            self.remove_floor(self.current_floor)
            self.is_moving = False
            self.open_door()

    def has_reached_top(self):
        return self.direction == Direction.UP.value and self.current_floor == max(self.target_floors)
    
    def has_reached_bottom(self):
        return self.direction == Direction.DOWN.value and self.current_floor == min(self.target_floors)

    def get_distance(self, floor):
        return abs(self.current_floor - floor)

    def is_moving_toward(self, from_floor: int, direction: Direction):
        if direction == Direction.UP.value and self.direction == Direction.UP.value and self.current_floor <= from_floor:
            return True
        
        if direction == Direction.DOWN.value and self.direction == Direction.DOWN.value and self.current_floor >= from_floor:
            return True
        
        return False
    
    def is_higher_than(self, floor: int):
        return self.current_floor > floor
    
    def dict(self):
        return self.__dict__