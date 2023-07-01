import time

from core import encore_api
from core import logging

import configparser
import multiprocessing


class Worker(encore_api.Module):
    def __init__(self, process_name: str, config: configparser.ConfigParser, logger: logging.Logger) -> None:
        self.config = config
        self.logger = logger

        super().__init__(process_name=process_name)

        self.logger(
            f'Module {self.__class__.__name__}:{process_name} has been connected'
        )

    def run(self, queue: multiprocessing.Queue) -> None:
        while True:
            time.sleep(1)
            self.logger(f'Worker: {queue.qsize()}')