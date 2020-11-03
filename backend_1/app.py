from fastapi import FastAPI
from pydantic import BaseModel
import requests


app = FastAPI(title="Backend # 1")


@app.get("/")
async def root():
    return {"message": "Hello World"}
    

class Numbers(BaseModel):
    x: float
    y: float

@app.post('/run_task')
def enqueue_add_back_2(n: Numbers):

    inp_post_response = requests.post("http://0.0.0.0:8080/run_task", json={"x":n.x,"y":n.y})
    
    if inp_post_response .status_code == 200:
       return {"message": "Send work to Backend 2"}
    else:
        return {"message":"Error send task to Backend 2"}
