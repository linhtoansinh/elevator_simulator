from ..constants import MAX_PEOPLE, NUM_FLOORS
from ..enums.directions import Direction

class Elevator:
    def __init__(self, elevator_id, current_floor=1, direction=None, num_passengers=0, is_open=False):
        self.elevator_id = elevator_id
        self.current_floor = current_floor
        self.direction = direction
        self.num_passengers = num_passengers
        self.is_open = is_open
        self.target_floors = set()

    def add_passenger(self, num_passengers):
        self.num_passengers += min(num_passengers, MAX_PEOPLE - self.num_passengers) if len(self.num_passengers) < MAX_PEOPLE else 0

    def remove_passenger(self, num_passengers):
        self.num_passengers = self.num_passengers - num_passengers if self.num_passengers > num_passengers else 0

    def add_floor(self, floors=[]):
        self.target_floors.update(floors)

    def remove_floor(self, floor):
        self.target_floors.discard(floor)

    def is_full(self):
        return self.num_passengers >= MAX_PEOPLE

    def open_doors(self):
        self.is_open = True

    def close_doors(self):
        self.is_open = False

    def move_up(self):
        if self.target_floors and self.current_floor < NUM_FLOORS:
            self.current_floor += 1
            self.direction = Direction.UP

    def move_down(self):
        if self.target_floors and self.current_floor > 1:
            self.current_floor -= 1
            self.direction = Direction.DOWN

    def get_distance(self, floor):
        return abs(self.current_floor - floor)
