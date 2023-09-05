from settings.localisation import VITAL_MESSAGES_FIELDS, check_field
from configparser import ConfigParser
from encorelib.timer import Timer
from dotenv import load_dotenv
from encorelib import logging
from core import errhandler
from core.cli import text
from core.cli import menu
import os

load_dotenv()


def main():
    timer = Timer()
    # -----------------------------
    # 0) Load .env and check fields
    # -----------------------------
    timer.start('Checking dotenv')

    settings = ConfigParser()
    if os.path.exists('.env'):
        if 'SETTINGS_DIR' in os.environ:
            settings.read(os.getenv('SETTINGS_DIR'))
        else:
            errhandler.error('0x000001')
    else:
        errhandler.error('0x000000')

    # Hyperparameters
    VERSION = settings['General']['version']
    WIDTH = int(settings['Terminal']['width'])
    HEIGHT = int(settings['Terminal']['height'])

    timer.end('Checking dotenv')
    # -----------------------------
    # 1) Set localisation
    # -----------------------------
    timer.start('Setting language')

    language = ConfigParser()
    language_path = settings['General']['language']
    if os.path.exists(language_path):
        language.read(language_path)
        # Check messages
        for field in VITAL_MESSAGES_FIELDS['Logger']:
            errhandler.safe_call(check_field, '0x000002', language, 'Logger', field)

        for field in VITAL_MESSAGES_FIELDS['Terminal']:
            errhandler.safe_call(check_field, '0x000002', language, 'Terminal', field)
    del language_path, field

    timer.end('Setting language')
    # -----------------------------
    # 2) Initialize logger
    # -----------------------------
    timer.start('Initializing logger')

    logger = logging.Logger(settings)
    logger.info('AITrading terminal: Hello, World!')

    timer.end('Initializing logger')
    # -----------------------------
    # 3) Greeting
    # -----------------------------
    timer.start('Greeting')

    if settings['Terminal']['show_logo'].lower() == 'true':
        print(text.logo)
    timer.end('Greeting')

    # -----------------------------
    # 4) Start terminal echo
    # -----------------------------
    timer.start('Session')

    colorscheme = ConfigParser()
    if settings['General']['use_cli'].lower() == 'true':
        colorscheme.read(settings['Terminal']['colorscheme'])

        while True:
            result = menu.run(
                width       = int(settings['Terminal']['width']),
                height      = int(settings['Terminal']['height']),
                colorscheme = colorscheme,
            )
            if not result:
                break
            elif result[0] == 'select dataset':
                while True:
                    files = os.listdir(settings['Assets']['datasets'])
                    for i, file in files:
                        print(f'{i+1}) {file}')
                    carrier = input('>>>')
                    if carrier == '0':
                        break
                    elif carrier.isdigit():
                        if int(carrier) < len(files):
                            dataset_path = files[int(carrier)]


    timer.end('Session')
    # -----------------------------
    # n) Clear last N logs
    # -----------------------------
    logging_path = settings['Logging']['logging_path']
    leave_last_n = int(settings['Logging']['leave_last_n'])
    for log_name in os.listdir(logging_path)[:-leave_last_n]:
        os.remove(os.path.join(logging_path, log_name))

    # -----------------------------
    # n+1) Show timer
    # -----------------------------
    if settings['Terminal']['show_timer'].lower() == 'true':
        print(timer)
    del timer



if __name__ == '__main__':
    main()
