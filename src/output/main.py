import logging
import json
from utils.mq_agent import MessageQueueAgent
from utils.constants import OUTPUT_QUEUE, TEXT_TO_SPEECH_QUEUE
from create_output_file import create_file


def _initialize():
    logging.basicConfig(level=logging.INFO)


def send_message(message):
    mq_agent = MessageQueueAgent()
    mq_agent.publish_message(json.dumps(message), TEXT_TO_SPEECH_QUEUE)
    print(f'Message sent: {message}')


def callback(ch, method, properties, body):
    try:
        message = body.decode()
        source = json.loads(message).get('source')
        content = json.loads(message).get('message')
        logging.info(message)
        create_file(content, source)
        send_message(json.loads(message))
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