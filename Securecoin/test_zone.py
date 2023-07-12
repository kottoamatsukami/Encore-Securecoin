from configparser import ConfigParser
from core import cli_updated
from core.cli_updated import text
import os
import sys
import time


def greeting(config: ConfigParser) -> None:
    # Change terminal size
    sys.stdout.write("\x1b[8;{rows};{cols}t".format(rows=50, cols=150))
    if config['Menu']['skip_logo'].lower() == 'true':
        return None
    os.system('cls')
    # Print Logo
    print(text.logo)
    time.sleep(float(config['Menu']['pre_product_show_delay']))
    for line in text.product.format(config['Menu']['version']).split('\n'):
        print(line)
        time.sleep(float(config['Menu']['show_product_timestamps']))
    time.sleep(float(config['Menu']['post_product_show_delay']))


config = ConfigParser()
config.read('./data/config.ini')

locale = ConfigParser()
locale.read('./data/localisation/eng')
color_scheme = ConfigParser()
color_scheme.read('./data/console_styles/classic')


greeting(config)
menu_template = cli_updated.Menu(
    title=cli_updated.Title(
        main_text=text.menu, fill_char=' ',
        hint_1='< Securecoin >', char_1='-',
        hint_2='[ Choose one option below]', char_2='-'
    ),
    name='init',
    options=(
        cli_updated.Menu(
            title=cli_updated.Title(
                main_text='SUBMENU'
            ),
            name='Submenu',
            options=(
                cli_updated.Option(
                    name='Option 1',
                ),
                cli_updated.Option(
                    name='Option 2',
                ),
                cli_updated.Option(
                    name='Option 3',
                ),
            ),
            style=color_scheme,
            locale=locale,
        ),
        cli_updated.MultiSelectionMenu(
            title=cli_updated.Title(
                main_text='MULTI-MENU',
            ),
            name='Multi Selection Test',
            options=(
                cli_updated.Option(
                    name='Option 1',
                ),
                cli_updated.Option(
                    name='Option 2',
                ),
                cli_updated.Option(
                    name='Option 3',
                ),
            ),
            style=color_scheme,
            locale=locale
        )

    ),
    style=color_scheme,
    locale=locale
)
menu = cli_updated.MenuAgregator(
    root=menu_template,
)
menu.run(150)

