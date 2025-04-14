from pymongo import MongoClient
import os
from dotenv import load_dotenv

cwd = os.path.abspath(os.path.dirname(__file__))
load_dotenv("{}/../.env".format(cwd))

client = MongoClient(os.environ["MONGO_URL"])
db = client[os.environ["MONGO_DB_NAME"]]