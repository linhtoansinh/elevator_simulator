from ..models.elevator import Elevator
from ..constants import NUM_ELEVATORS
from ..enums.directions import Direction

class ElevatorService:
    def __init__(self):
        self.elevators = [Elevator(i) for i in range(0, NUM_ELEVATORS)]

    def find_best_elevator(self, from_floor, direction):
        best_elevator = self.elevators[0]
        min_distance = float('inf')

        for elevator in self.elevators:
            if direction == Direction.UP and elevator.direction == Direction.DOWN and elevator.current_floor > from_floor:
                continue
            if direction == Direction.DOWN and elevator.direction == Direction.UP and elevator.current_floor < from_floor:
                continue

            distance = elevator.get_distance(from_floor)
            if distance < min_distance and not elevator.is_full():
                best_elevator = elevator
                min_distance = distance

        return best_elevator

    def open_door(self, elevator_id: int):
        if 0 <= elevator_id < NUM_ELEVATORS:
            self.elevators[elevator_id].open_doors()
            return True
        return False
    
    def close_door(self, elevator_id: int):
        if 0 <= elevator_id < NUM_ELEVATORS:
            self.elevators[elevator_id].close_doors()
            return True
        return False
