from elevator.models.elevator_mongo import Elevator
from ..database import db
from ..dtos.elevator_update_dto import ElevatorUpdateDto

class ElevatorRepository:
    def __init__(self):
        self.collection = db["elevators"]
        pass

    def update(self, elevator_id: int, document: ElevatorUpdateDto):
        self.collection.update_one({"elevator_id": elevator_id}, {"$set": document.dict()})

    def get_all(self) -> list[Elevator]:
        elevators = self.collection.find()
        return [Elevator.model_validate(elevator) for elevator in elevators]
    