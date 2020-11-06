from fastapi import FastAPI, WebSocket, BackgroundTasks
from fastapi.responses import HTMLResponse
import json
import requests

try:
    import pika
    import ast

except Exception as e:
    print("Sone Modules are missings {}".format_map(e))

class MetaClass(type):

    _instance ={}

    def __call__(cls, *args, **kwargs):
        # Singelton Design Pattern  
        if cls not in cls._instance:
            cls._instance[cls] = super(MetaClass, cls).__call__(*args, **kwargs)
            return cls._instance[cls]

class RabbitMqServerConfigure(metaclass=MetaClass):

    def __init__(self, host='localhost',queue='hello'):
        """ Server initialization """
        self.host = host
        self.queue = queue


class rabbitmqServer():

    def __init__(self,server):
        """
        :param server : Object of class RabbitMqServerConfigure

        """

        self.server = server
        self._connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.server.host))
        self._channel = self._connection.channel()
        self._tem = self._channel.queue_declare(queue=self.server.queue)
        print("Server started waiting for Messages ")
    
    @staticmethod
    def callback(ch, method, properties, body):
        global result
        payload = body.decode("utf-8")
        payload = ast.literal_eval(payload)
        print("Data Received : {}".format(payload))
        


    def startServer(self):
        self._channel.basic_consume(
            queue=self.server.queue,
            on_message_callback=rabbitmqServer.callback,
            auto_ack=False)
        self._channel.start_consuming()


def consumer(l=""):
    serverConfigure = RabbitMqServerConfigure(host='localhost',queue='results')
    server = rabbitmqServer(server = serverConfigure)
    
    return server

app = FastAPI()

html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Sumas</title>
    </head>
    <body>
        <h1>Rabbitmq - Celery - Websockets Sumas</h1>
        <form action="" onsubmit="sendMessage(event)">
            X: <input type="text" id="x" autocomplete="off"/>
            <br>
            <br>
            Y: <input type="text" id="y" autocomplete="off"/>
            <br>
            <br>

            <button>Send</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
            var ws = new WebSocket("ws://localhost:8088/ws");

            ws.onmessage = function(event) {
                var messages = document.getElementById('messages')
                var message = document.createElement('li')
                var content = document.createTextNode(event.data)
                message.appendChild(content)
                messages.appendChild(message)
            };
            
            function sendMessage(event) {
                var x = document.getElementById("x")
                var y = document.getElementById("y")
                
                data = JSON.stringify({x:x.value,y:y.value})
                d = x.value+" "+y.value
                ws.send(data)
                x.value = ''
                y.value = ''
                event.preventDefault()
            }
        </script>
    </body>
</html>
"""


@app.get("/")
async def get():
    return HTMLResponse(html)

server = consumer()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket, background_tasks: BackgroundTasks):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        data = json.loads(data)
        
        
        background_tasks.add_task(server.startServer)

        r = int(data["x"])+int(data["y"])        

        inp_post_response = requests.post("http://0.0.0.0:8081/run_task", json={"x":data["x"],"y":data["y"]})

        print(inp_post_response)
        #await websocket.send_text()
        print(server.result)

        await websocket.send_text(f"Message text was: {data['x']+' + '+data['y']+' = '+str(r)}")