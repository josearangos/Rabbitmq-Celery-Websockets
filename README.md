# Rabbitmq-Celery-Websockets

## Backend_1

0. pip install -r requeriments.txt
1. Run rabbitmq : docker run --rm -it --hostname rabbit-container -p 15672:15672 -p 5672:5672 rabbitmq:3-management
2. Run celery: celery worker -A worker.celery_app  -l info -Q add
3. python main.py
4. show web broser : http://0.0.0.0:8080/docs
5. Rabbitmq: http://localhost:15672/  user: guest passwd: guest
6. RUn frontend: python3 run.py



