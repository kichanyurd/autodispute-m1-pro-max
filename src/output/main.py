import logging
import json
from utils.mq_agent import MessageQueueAgent
from utils.constants import OUTPUT_QUEUE
from create_output_file import create_file


def _initialize():
    logging.basicConfig(level=logging.INFO)


def callback(ch, method, properties, body):
    try:
        message = body.decode()
        source = json.loads(message).get('source')
        content = json.loads(message).get('message')
        logging.info(message)
        create_file(content, source)
    except:
        logging.exception("An error occured")


def handler():
    mq_agent = MessageQueueAgent()
    logging.info("Starting consumer")
    mq_agent.add_consumer(callback, OUTPUT_QUEUE)
    mq_agent.start_consuming()


if __name__ == '__main__':
    _initialize()
    handler()