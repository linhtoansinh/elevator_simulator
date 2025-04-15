from django.core.management.base import BaseCommand, CommandError

from elevator.constants import NUM_ELEVATORS
from elevator.models.elevator_mongo import Elevator
from elevator.database import db
from pymongo.errors import OperationFailure

class Command(BaseCommand):
    help = "Populate new elevators to mongodb"

    def handle(self, *args, **options):
        existed = True
        try:
            db.validate_collection("elevators")
        except OperationFailure:
            existed = False

        if not existed:
            try:
                db.create_collection("elevators")
                collection = db["elevators"]

                for i in range(NUM_ELEVATORS):
                    elevator = {
                        "elevator_id": i,
                        "current_floor": 1,
                        "direction": None,
                        "is_open": False,
                        "target_floors": [],
                        "is_moving":  False
                    }
                    collection.insert_one(elevator)

                self.stdout.write(
                    self.style.SUCCESS('Successfully')
                )
            except Exception as e:
                raise CommandError(e)