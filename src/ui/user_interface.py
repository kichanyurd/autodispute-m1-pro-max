import json
import sys
import time
from utils.constants import ORCHESTRATOR_QUEUE, OUTPUT_QUEUE
from utils.mq_agent import MessageQueueAgent


class UserInterface:
    def __init__(self):
        self._menu = {
            '1': 'Send a message',
            '2': 'Exit',
        }

    def display_menu(self):
        print('Menu:')
        for key, value in self._menu.items():
            print(f'{key}. {value}')

    def get_user_choice(self):
        choice = input('Enter your choice: ')
        return choice

    def send_a_message(self, message=None):
        if message:
            description = message
        else:
            description = input('Enter the task description: ')
        queue_message = {
            'source': 'UserInterface',
            'description': description
        }
        mq_agent = MessageQueueAgent()
        mq_agent.publish_message(json.dumps(queue_message), ORCHESTRATOR_QUEUE)
        mq_agent.publish_message(json.dumps(queue_message), OUTPUT_QUEUE)
        print(f'Message sent: {queue_message}')
        return description


if __name__ == "__main__":
    ui = UserInterface()
    time.sleep(3)
    ui.send_a_message("orchestrator")
    # ui.display_menu()
    # choice = ui.get_user_choice()
    # print(f'You chose {choice}')
    # if choice == '1':
    #     ui.send_a_message()
    # elif choice == '2':
    #     sys.exit(0)