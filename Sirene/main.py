from core.utils import DirectoryManager
from core.app import app
import flet as ft
import os


def main():
    # 0) Check dirs
    ROOT_PATH = os.getcwd()
    DirectoryManager(ROOT_PATH).check_directories()

    # 1) Run app
    ft.app(
        target=app,
        name='Sirene',
    )


if __name__ == '__main__':
    main()
