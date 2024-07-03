import pika
import logging
from retry import retry
from utils.constants import HOST


class MessageQueueAgent():
    def __init__(self) -> None:
        pika_logger = logging.getLogger("pika")
        pika_logger.setLevel(logging.WARNING)
        self.connection = self._get_connection()
        self.channel = self.connection.channel()

    @retry(pika.exceptions.AMQPConnectionError, delay=5, jitter=(1, 3))
    def _get_connection(self):
        return pika.BlockingConnection(pika.ConnectionParameters(HOST))
    
    def publish_message(self, message, queue):
        self.channel.queue_declare(queue=queue)
        self.channel.basic_publish(exchange='',
                                    routing_key=queue,
                                    body=message)
        logging.info("Message published")

    def add_consumer(self, callback_function, queue):
        self.channel.queue_declare(queue=queue)
        self.channel.basic_consume(queue=queue,
                            auto_ack=True,
                            on_message_callback=callback_function)

    def start_consuming(self):
        self.channel.start_consuming()