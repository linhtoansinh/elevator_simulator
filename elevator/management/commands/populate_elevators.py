from django.core.management.base import BaseCommand, CommandError

from elevator.constants import NUM_ELEVATORS
from elevator.models.elevator_mongo import Elevator
from elevator.database import db

class Command(BaseCommand):
    help = "Populate new elevators to mongodb"

    def handle(self, *args, **options):
        try:
            collection = db["elevators"]

            collection.drop()
            db.create_collection("elevators")

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