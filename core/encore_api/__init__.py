from core import logging


import configparser
import multiprocessing
import threading
import time


class Module(object):
    def __init__(self, process_name: str) -> None:
        self.process_name = process_name

    def run(self, queue: multiprocessing.Queue) -> None:
        print(f'{self.__repr__()} <run> function is not implemented')

    def __repr__(self) -> str:
        return f'Module: {self.__class__.__name__}:{self.process_name}'


class Application(object):
    def __init__(self, *modules, config: configparser.ConfigParser, logger: logging.Logger) -> None:
        assert all(isinstance(module, Module) for module in modules)
        self.modules = modules
        self.config = config
        self.logger = logger

        self.logger(f'The application has initialized the modules')

        self.processes = {}
        self.queue = multiprocessing.Queue()

    def run(self) -> None:
        self.queue = multiprocessing.Queue()
        self.processes = {}

        # Main modules initialization
        for module in self.modules:
            self.run_module(module)

        self.logger(f'The application has been started')
        for process in self.processes.values():
            process.join()
        self.logger(f'The application has been stopped')

    def restart_process(self, process_name) -> None:
        if process_name in self.processes:
            self.logger.info(f'{process_name} is restarting...')
            self.processes[process_name].terminate()
            self.processes[process_name].run()
            self.logger.info(f'{process_name}: restarting complete')
        else:
            self.logger.error(f'{process_name} not in running processes')

    def run_module(self, module):
        if isinstance(module, str):
            self.logger.info(f'{module} is running...')
            self.processes[module].start()
            self.logger.info(f'{module}: Running complete')

        elif isinstance(module, Module):
            self.logger.info(f'{module} is running...')
            process = multiprocessing.Process(
                target=module.run,
                args=(self.queue,)
            )
            self.processes[module.process_name] = process
            process.start()
            self.logger.info(f'{module}: Running complete')