from configparser import ConfigParser
from core.logging import Logger
import time
import os


class TimeManager(object):
    def __init__(self):
        self.timer = {}

    def start(self, name: str) -> float:
        self.timer[name] = (time.time(), 0)
        return self.timer[name][0]

    def end(self, name: str) -> float:
        self.timer[name] = (self.timer[name][0], time.time())
        return self.timer[name][1]

    def __repr__(self) -> str:
        log = '-----<Timer>-----\n'
        for name in self.timer:
            log += f'[{name}]: {self.timer[name][1]-self.timer[name][0]:.7f}\n'
        return log


class OSManager(object):
    def __init__(self, root_path: str, config: ConfigParser, logger: Logger) -> None:
        self.root_path = root_path
        self.config = config
        self.logger = logger

        self.logger(f'{self.__class__.__name__} has connected')

    def clear_dir(self, dir_path: str, deep: bool) -> None:
        path = os.path.join(self.root_path, dir_path) if dir_path[0] != '.' else dir_path
        os.chmod(path, 777)
        self.logger.info(f'[{self.__class__.__name__}]: Try to clear directory {path}')
        if os.path.exists(path):
            for subdir in os.listdir(path)[:-int(self.config['Options']['num_of_logs'])]:
                subpath = os.path.join(path, subdir)
                if os.path.isdir(subpath) and deep:
                    self.clear_dir(subpath, deep)
                else:
                    os.remove(subpath)
                    self.logger(f'[{self.__class__.__name__}]: {subpath} was removed')
            self.logger(f'[{self.__class__.__name__}]: Completed')
        else:
            self.logger.error(f'[{self.__class__.__name__}]: Directory {path} is not found')
