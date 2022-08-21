from celery import Celery
from dotenv import load_dotenv, find_dotenv
import os

load_dotenv(find_dotenv())

username = os.environ.get("MONGODB_USER")

password = os.environ.get("MONGODB_PWD")

connection_string = F"mongodb+srv://{username}:{password}@firstmongo.oday65l.mongodb.net/?retryWrites=true&w=majority"

app = Celery('worker', backend=connection_string, broker='redis://localhost', include=['tasks'])


class CeleryConfig:
    task_serializer = "pickle"
    result_serializer = "pickle"
    event_serializer = "json"
    accept_content = ["application/json", "application/x-python-serialize"]
    result_accept_content = ["application/json", "application/x-python-serialize"]


app.config_from_object(CeleryConfig)
