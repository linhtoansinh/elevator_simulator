from elevator.models.elevator_mongo import Elevator
from ..database import db

class ElevatorRepository:
    def __init__(self):
        self.collection = db["elevators"]
        pass

    def update(self, elevator_id: int, document):
        self.collection.update_one({"elevator_id": elevator_id}, {"$set": document})

    def get_all(self) -> list[Elevator]:
        elevators = self.collection.find()
        return [Elevator.model_validate(elevator) for elevator in elevators]
    
    def get(self, id) -> Elevator | None:
        elevator = self.collection.find({"elevator_id": id})
        return Elevator.model_validate(elevator[0]) if elevator else None