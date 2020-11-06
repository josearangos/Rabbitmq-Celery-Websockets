

from flask import render_template
from flask_socketio import emit
from app import app, socketio
import random
import requests

import pika
from threading import Lock

def rabbit_callback(ch, method, properties, body):
    print(body)
    emit('my_response', {'data': 'yes'})
    print("body: ", body)



def connect_rabbitmq():
    cred = pika.credentials.PlainCredentials('guest', 'guest')
    conn_param = pika.ConnectionParameters(host='localhost',
                                           credentials=cred)
    connection = pika.BlockingConnection(conn_param)
    channel = connection.channel()

    #channel.exchange_declare(exchange='ncs', exchange_type='fanout')

    channel.queue_bind(exchange='default', queue='results')
    
    channel.basic_consume(rabbit_callback, queue='results', no_ack=True)
    
    return channel

def get_messages():
    channel = connect_rabbitmq()
    channel.start_consuming()


numbers_to_add = []

thread = None
thread_lock = Lock()




@app.route('/')
def home():
    return render_template('index.html')


@socketio.on('connect')
def test_connect():
    global thread
    with thread_lock:
        if thread is None:
            thread = socketio.start_background_task(target=get_messages)

    emit('my_response', {'data': 'Connected', 'count': 0})
    print('connected')


"""
@socketio.on('connect')
def connect():  

    print("Usuario Conectado!!!")


"""

@socketio.on('sendTask')
def sendTask(n):
    #Llamar al backend 1 
    inp_post_response = requests.post("http://0.0.0.0:8081/run_task", json={"x":n["x"],"y":n["y"]})
    if inp_post_response .status_code == 200:
        n["status"] = "PROCESSING"
    numbers_to_add.append(n)         
    emit('tasks',numbers_to_add,broadcast=True)
