import asyncio
from ..models.elevator import Elevator
from ..constants import NUM_ELEVATORS
from ..enums.directions import Direction
from ..enums.door_states import DoorState
from queue import Queue
from channels.layers import get_channel_layer

channel_layer = get_channel_layer()
class ElevatorService:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(ElevatorService, cls).__new__(cls, *args, **kwargs)
        return cls._instance
    
    def __init__(self):
        if not hasattr(self, 'initialized'):
            self.elevators = [Elevator(i) for i in range(0, NUM_ELEVATORS)]
            self.requests_queue = Queue()
            self.initialized = True

    def find_best_elevator(self, from_floor: int, direction: Direction):
        best_elevator = None
        min_distance = float('inf')

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

            if best_elevator.direction is None:
                best_elevator.direction = Direction.DOWN.value if best_elevator.is_higher_than(from_floor) else Direction.UP.value
        else:
            self.requests_queue.put((from_floor, direction))

    def request_floors(self, elevator_id: int, floors: list[int]):
        elevator = self.elevators[elevator_id]
        elevator.add_floors(floors)
        if elevator.direction is None:
            elevator.direction = Direction.DOWN.value if elevator.is_higher_than(floors[0]) else Direction.UP.value

    def request_door(self, elevator_id: int, action: str):
        if action == DoorState.OPEN.value:
            self.elevators[elevator_id].open_door()
        else:
            self.elevators[elevator_id].close_door()

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
            elevator.move()
            await self.send_elevator_update(elevator)
            await asyncio.sleep(2)
    
    async def send_elevator_update(self, elevator: Elevator):
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