import logging
import json
from utils.mq_agent import MessageQueueAgent
from utils.constants import ORCHESTRATOR_QUEUE, OUTPUT_QUEUE, LLM_WORKER_1_QUEUE

def _initialize():
    logging.basicConfig(level=logging.INFO)


def callback(ch, method, properties, body):
    try:
        logging.info(f"Received {body}")
        logging.info(body.decode())
        send_message()
    except:
        logging.exception("An error occured")


def send_message():
    mq_agent = MessageQueueAgent()
    queue_message = {
        'source': 'orchestrator',
        'message': 'llm-1'
    }
    mq_agent.publish_message(json.dumps(queue_message), LLM_WORKER_1_QUEUE)
    mq_agent.publish_message(json.dumps(queue_message), OUTPUT_QUEUE)
    print(f'Message sent: {queue_message}')


def handler():
    mq_agent = MessageQueueAgent()
    logging.info("Starting consumer")
    mq_agent.add_consumer(callback, ORCHESTRATOR_QUEUE)
    mq_agent.start_consuming()


if __name__ == '__main__':
    _initialize()
    handler()