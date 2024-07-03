import logging
import json
from utils.mq_agent import MessageQueueAgent
from utils.constants import LLM_WORKER_3_QUEUE

def _initialize():
    logging.basicConfig(level=logging.INFO)


def callback(ch, method, properties, body):
    try:
        logging.info(f"Received {body}")
        logging.info(body.decode())
    except:
        logging.exception("An error occured")


def handler():
    mq_agent = MessageQueueAgent()
    logging.info("Starting consumer")
    mq_agent.add_consumer(callback, LLM_WORKER_3_QUEUE)
    mq_agent.start_consuming()


if __name__ == '__main__':
    _initialize()
    handler()