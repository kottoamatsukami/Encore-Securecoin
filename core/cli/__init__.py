import multiprocessing

from core import encore_api
from core import logging

from core.cli import text

import configparser
import sys


class CLI(encore_api.Module):
    def __init__(self, process_name: str, config: configparser.ConfigParser, logger: logging.Logger) -> None:
        self.config = config
        self.logger = logger

        super().__init__(process_name=process_name)

        self.logger(
            f'Module {self.__class__.__name__}:{process_name} has been connected'
        )

    def run(self, queue: multiprocessing.Queue) -> None:
        sys.stdin = open(0) # We get an EOF error without this line

        # Get the Logo
        #print(text.logo)
        while True:
            # Get the main menu
            print(text.main_menu)
            menu_carrier = text.get_input(flag='CLI')
            if menu_carrier == '0':
                # Exit
                exit()
            elif menu_carrier == '1':
                # Send message to all users
                print('Send message to all users')
            elif menu_carrier == '2':
                # Get length of queue
                print('Get length of queue')
            elif menu_carrier == '3':
                # Pure CLI
                while True:
                    command = text.get_input(flag='Pure CLI')
                    if command.lower() in ('exit', 'back', 'return', 'quit'):
                        break
                    else:
                        queue.put(
                            ('daemon', command.strip())
                        )

            else:
                continue
