import asyncio

from ..repositories.elevator_repository import ElevatorRepository
from ..models.elevator import Elevator
from ..constants import NUM_ELEVATORS
from ..enums.directions import Direction
from ..enums.door_states import DoorState
from queue import Queue
from channels.layers import get_channel_layer

channel_layer = get_channel_layer()

class ElevatorServiceMongo:
    def __init__(self):
        self.repository = ElevatorRepository()
        self.elevators = self.repository.get_all()
        self.requests_queue = Queue()
        self.initialized = True

    def find_best_elevator(self, from_floor: int, direction: Direction):
        best_elevator = None
        min_distance = float('inf')

        self.elevators = self.repository.get_all()
        for elevator in self.elevators:
            if elevator.direction is None and not elevator.is_open:
                distance = elevator.get_distance(from_floor)
                if distance < min_distance:
                    best_elevator = elevator
                    min_distance = distance
            elif elevator.is_moving_toward(from_floor, direction):
                distance = elevator.get_distance(from_floor)
                if distance < min_distance:
                    best_elevator = elevator
                    min_distance = distance

        return best_elevator

    def handle_request(self, from_floor: int, direction: Direction):
        best_elevator = self.find_best_elevator(from_floor, direction)
        if best_elevator and best_elevator.current_floor != from_floor:
            best_elevator.add_floors([from_floor])
            self.repository.update(best_elevator.elevator_id, {
                "target_floors": best_elevator.target_floors
            })

            if best_elevator.direction is None:
                best_elevator.direction = Direction.DOWN.value if best_elevator.is_higher_than(from_floor) else Direction.UP.value
                self.repository.update(best_elevator.elevator_id, {
                    "direction": best_elevator.direction
                })
        else:
            self.requests_queue.put((from_floor, direction))

    def request_floors(self, elevator_id: int, floors: list[int]):
        elevator = self.repository.get(elevator_id)

        elevator.add_floors(floors)
        if elevator.direction is None:
            elevator.direction = Direction.DOWN.value if elevator.is_higher_than(floors[0]) else Direction.UP.value

        self.repository.update(elevator_id, {
            "target_floors": elevator.target_floors,
            "direction": elevator.direction
        })

    def request_door(self, elevator_id: int, action: str):
        if action == DoorState.OPEN.value:
            self.repository.update(elevator_id, {
                "is_open": True
            })
        else:
            self.repository.update(elevator_id, {
                "is_open": False
            })


    def move(self, elevator_id):
        elevator = self.repository.get(elevator_id)

        if len(elevator.target_floors) < 1:
            self.repository.update(elevator.elevator_id, {
                "direction": None,
                "is_moving": False
            })

            return
        
        if elevator.is_open:
            return

        _elevator = {}
        _elevator["is_moving"] = True
        _elevator["current_floor"] = elevator.current_floor

        if elevator.direction == Direction.UP.value and elevator.current_floor < max(elevator.target_floors):
            elevator.current_floor += 1
            _elevator["current_floor"] += 1
        elif elevator.direction == Direction.DOWN.value and elevator.current_floor > min(elevator.target_floors):
            elevator.current_floor -= 1
            _elevator["current_floor"] -= 1

        if elevator.has_reached_top() and len(elevator.target_floors) > 1:
            elevator.direction = Direction.DOWN.value
            _elevator["direction"] = Direction.DOWN.value

        if elevator.has_reached_bottom() and len(elevator.target_floors) > 1:
            elevator.direction = Direction.UP.value
            _elevator["direction"] = Direction.UP.value

        if elevator.current_floor in elevator.target_floors:
            elevator.remove_floor(elevator.current_floor)
            elevator.is_moving = False
            elevator.open_door()

            _elevator["target_floors"] = elevator.target_floors
            _elevator["is_moving"] = elevator.is_moving
            _elevator["is_open"] = elevator.is_open

        self.repository.update(elevator.elevator_id, _elevator)

    async def handle_queue(self):
        while True:
            if not self.requests_queue.empty():
                request = self.requests_queue.get()
                
                if request:
                    from_floor, direction = request
                    best_elevator = self.find_best_elevator(from_floor, direction)
                    
                    if best_elevator is None:
                        self.requests_queue.put(request)
                    elif best_elevator.current_floor != from_floor:
                        best_elevator.add_floors([from_floor])
                        if best_elevator.direction is None:
                            best_elevator.direction = Direction.DOWN.value if best_elevator.is_higher_than(from_floor) else Direction.UP.value
                        
            await asyncio.sleep(1)

    async def move_elevator(self, elevator: Elevator):
        while True:
            self.move(elevator.elevator_id)

            await self.send_elevator_update(elevator.elevator_id)
            await asyncio.sleep(2)
    
    async def send_elevator_update(self, elevator_id):
        elevator = self.repository.get(elevator_id)

        await channel_layer.group_send(
            "elevators",
            {
                "type": "send_elevators",
                "elevator": {
                    "id": elevator.elevator_id,
                    "current_floor": elevator.current_floor,
                    "direction": elevator.direction,
                    "is_moving": elevator.is_moving,
                    "is_open": elevator.is_open
                }
            }
        )

    async def start_moving_elevators(self):
        for elevator in self.elevators:
            asyncio.create_task(self.move_elevator(elevator))