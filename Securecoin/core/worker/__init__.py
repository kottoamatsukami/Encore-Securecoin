from core.bots.dex_loan_arbitrage import D
from configparser import ConfigParser
from core.logging import Logger
import multiprocessing
import time


class Worker(object):
    def __init__(self, config: ConfigParser, logger: Logger) -> None:
        self.config = config
        self.logger = logger
        self.working_queue = multiprocessing.Queue()
        self.output_queue = multiprocessing.Queue()
        self.is_working = False

    def add_work(self, work: list) -> None:
        self.working_queue.put(work)
        self.logger(f'append {work}')

    def start_daemon(self) -> None:
        self.is_working = True
        process = multiprocessing.Process(
            target=self.daemon,
            args=(),
        )
        process.start()

    def daemon(self) -> None:
        dex_flash_loan_bot = 9
        while True:
            if not self.is_working:
                break
            if self.working_queue.qsize() == 0:
                time.sleep(1)
                continue
            ###################################
            # WORK
            ###################################
            if self.working_queue.qsize() > 0:
                work = self.working_queue.get()
                if work[0] == 'DEX':
                    # DEX ARBITRAGE
                    menus = work[1:]
                    options = {
                        'Use Telegram Bot': True if any(menu.name == 'Use Telegram Bot' for menu in menus) else False,
                        'Use Flash Loan': True if any(menu.name == 'Use Flash Loan' for menu in menus) else False,
                        'Exchanges': [menu.name for menu in menus if menu.name not in ('Use Telegram Bot', 'Use Flash Loan')]
                    }
                    self.output_queue.put(options)

    def get_work(self) -> list:
        work_list = []
        while self.working_queue.qsize() > 0:
            work_list.append(self.working_queue.get())
        for work in work_list:
            self.working_queue.put(work)
        return work_list

    def get_output(self) -> list:
        output_list = []
        while self.output_queue.qsize() > 0:
            output_list.append(self.output_queue.get())
        return output_list
