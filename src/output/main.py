import logging
from utils.mq_agent import MessageQueueAgent
from utils.constants import OUTPUT_QUEUE

def _initialize():
    logging.basicConfig(level=logging.INFO)


def callback(ch, method, properties, body):
    try:
        logging.info(body.decode())
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