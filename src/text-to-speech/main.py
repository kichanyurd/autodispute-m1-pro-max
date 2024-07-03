import logging
from utils.mq_agent import MessageQueueAgent
from utils.constants import TEXT_TO_SPEECH_QUEUE
from polly_agent import text_to_speech 

def _initialize():
    logging.basicConfig(level=logging.INFO)


def callback(ch, method, properties, body):
    try:
        message = body.decode()
        logging.info(message)
        text_to_speech(message)
    except:
        logging.exception("An error occured")


def handler():
    mq_agent = MessageQueueAgent()
    logging.info("Starting consumer")
    mq_agent.add_consumer(callback, TEXT_TO_SPEECH_QUEUE)
    mq_agent.start_consuming()


if __name__ == '__main__':
    _initialize()
    handler()