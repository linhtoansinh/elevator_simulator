import asyncio
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from elevator.services.elevator_service_mongo import ElevatorServiceMongo
from ..services.elevator_service import ElevatorService
from ..constants import NUM_ELEVATORS, NUM_FLOORS

class ElevatorConsumer(AsyncJsonWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.elevator_service = ElevatorServiceMongo()

    async def connect(self):
        self.room_group_name = "elevators"
        
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        asyncio.create_task(self.elevator_service.start_moving_elevators())
        asyncio.create_task(self.elevator_service.handle_queue())

        await self.accept()

        await self.send_json({
            "num_floors": NUM_FLOORS,
            "num_elevators": NUM_ELEVATORS
        })

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive_json(self, content):
        if content["type"] == "request_elevator":
            self.elevator_service.handle_request(content["from_floor"], content["direction"])
        elif content["type"] == "request_floors":
            self.elevator_service.request_floors(content["elevator_id"], content["floors"])
        elif content["type"] == "request_door":
            self.elevator_service.request_door(content["elevator_id"], content["action"])

    async def send_elevators(self, event):
        await self.send_json({
            "elevator": event['elevator']
        })
