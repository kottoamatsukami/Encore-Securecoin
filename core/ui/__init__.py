import halo
import termcolor
import os


class UI(object):

    def __init__(self, config, system):
        self.config = config
        self.system = system

    def clear(self):
        if self.system == 'win':
            os.system('cls')
        else:
            os.system('clear')

    @staticmethod
    def get_choice() -> str or bool:
        return input('[echo]>>> ')

    @staticmethod
    def get_main_menu() -> None:
        print("""
                    <Encore Securecoin>
                      <Version - 0.1>
        |-----------------------------------------|
        |   1) Cite     # not working yet         |
        |   2) Server                             |
        |   0) Exit                               |
        |-----------------------------------------|""")

    @staticmethod
    def get_cite_menu() -> None:
        print('Nothing to show!')

    @staticmethod
    def get_server_menu() -> None:
        print("""
        |-----------------------------------------|
        |   1) Add    daemon                      |
        |   2) Remove daemon                      |
        |   3) Send command                       |
        |   4) Status                             |
        |   0) Back                               |
        |-----------------------------------------|""")

    @staticmethod
    def get_send_command_menu() -> None:
        print("""
        |-----------------------------------------|
        |   1) Get Parse Time                     |
        |   2) Stop working                       |
        |   3) Continue working                   |
        |   0) Back                               |
        |-----------------------------------------|""")



