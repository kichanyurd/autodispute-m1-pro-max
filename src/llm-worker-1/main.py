import logging
import json
from utils.mq_agent import MessageQueueAgent
from utils.constants import LLM_WORKER_1_QUEUE, LLM_WORKER_2_QUEUE, OUTPUT_QUEUE
import requests
from os.path import join

EMCIE_SERVER = "http://host.docker.internal:8000"
SESSION_ID = None

AGENT_NAME = "Default Agent"
"""
NOTE: Please ensure that the agent is configured with

{
    "when": "you're about to respond to any message",
    "then": "respond only if the last message contains the tag @<AGENT_NAME>"
}
"""

def _emcie_get_agent_id():
    response = requests.get(join(EMCIE_SERVER, "agents"))
    response.raise_for_status()
    agents = response.json()["agents"]
    return next(a for a in agents if a["name"] == AGENT_NAME)["id"]

def _emcie_new_session_id(agent_id):
    response = requests.post(join(EMCIE_SERVER, "sessions"), json={
        "agent_id": agent_id,
        "end_user_id": "User",
    })
    response.raise_for_status()
    return response.json()["session_id"]

def _emcie_post_message(source, message):
    response = requests.post(
        join(EMCIE_SERVER, "sessions", SESSION_ID, "events"),
        json={
            "content":  f"{source} said: {message}",
        }
    )
    response.raise_for_status()
    data = response.json()
    return data["event_id"], data["event_offset"]

def _emcie_get_new_messages(event_offset):
    response = requests.get(
        join(EMCIE_SERVER, "sessions", SESSION_ID, "events"),
        params={
            "min_offset": event_offset + 1,
            "wait": "true",
        }
    )
    response.raise_for_status()
    events = response.json()["events"]
    return [e["data"]["message"] for e in events if e["kind"] == "<message>"]

def _initialize():
    logging.basicConfig(level=logging.INFO)

def callback(ch, method, properties, body):
    try:
        logging.info(f"Received {body}")
        data = json.loads(body.decode())

        source = data["source"]
        message = data["message"]

        _, event_offset = _emcie_post_message(source, message)
        new_messages = _emcie_get_new_messages(event_offset)

        send_message("\n\n".join(new_messages))
    except:
        logging.exception("An error occured")

def send_message(message):
    mq_agent = MessageQueueAgent()
    queue_message = {
        'source': 'llm-1',
        'message': message,
    }
    mq_agent.publish_message(json.dumps(queue_message), LLM_WORKER_2_QUEUE)
    mq_agent.publish_message(json.dumps(queue_message), OUTPUT_QUEUE)
    print(f'Message sent: {queue_message}')

def handler():
    global SESSION_ID

    mq_agent = MessageQueueAgent()
    logging.info("Starting Emcie consumer") 

    agent_id = _emcie_get_agent_id()
    SESSION_ID = _emcie_new_session_id(agent_id)

    mq_agent.add_consumer(callback, LLM_WORKER_1_QUEUE)
    mq_agent.start_consuming()


if __name__ == '__main__':
    _initialize()
    handler()
