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
        payload = body.decode("utf-8")
        payload = ast.literal_eval(payload)
        print("Data Received : {}".format(payload))
        


    def startServer(self):
        self._channel.basic_consume(
            queue=self.server.queue,
            on_message_callback=rabbitmqServer.callback,
            auto_ack=False)
        self._channel.start_consuming()

if __name__ == "__main__":
    
    serverConfigure = RabbitMqServerConfigure(host='localhost',queue='results')
    server = rabbitmqServer(server = serverConfigure)
    server.startServer()