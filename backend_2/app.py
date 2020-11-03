import celery
from fastapi import FastAPI
from pydantic import BaseModel

#from worker import add
from celery_config import celery_app


app = FastAPI(title="Backend #2")

class Numbers(BaseModel):
    x: float
    y: float


@app.post('/run_task')
def enqueue_add(n: Numbers):
    # We use celery delay method in order to enqueue the task with the given parameter
    task_name = "worker.add"
    task = celery_app.send_task(task_name,args=[n.x,n.y],queue="add")
    #add.apply_async((n.x,n.y),queue='add',routing_key='add')
    return {"message": "Working!!"}


