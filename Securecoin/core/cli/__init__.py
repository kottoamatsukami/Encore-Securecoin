from configparser import ConfigParser
from core.logging import Logger
from core.cli_updated import text
from msvcrt import getch
import termcolor
import pprint
import time
import sys
import os

keyboard = {
    # (KEYS)   W A S D -> 119 97 115 100
    # (ARROWS) U D L R -> 72 80 75 77
    # (KEYPAD) U D L R -> 56 50 52 54
    # ENTER SPACE KP_ENTER -> 13 32 13
    # BACKSPACE DEL -> 8 83
    119: 'W', 97: 'A', 115: 'S', 100: 'D',
    72: 'UP_ARROW', 80: 'DOWN_ARROW', 75: 'LEFT_ARROW', 77: 'RIGHT_ARROW',
    56: 'KP_UP', 50: 'KP_DOWN', 52: 'KP_LEFT', 54: 'KP_RIGHT',
    13: 'ENTER', 32: 'SPACE', 8: 'BACKSPACE', 83: 'DEL',
}


class Menu(object):
    def __init__(
            self,
            name: str,
            colors: list[str],
            styles: list[str],
            additional_text=None,
            parent=None,
            multiple_choice=False,
            use_ind=True,
            arrow=' -> ',
    ) -> None:
        # Styles = bold, dark, underline, blink, reverse, and concealed
        #         |-> F|B selected
        # Colors: --> F|B not selected
        #         \-> F|B current selection
        self.name = name
        self.additional_text = additional_text
        self.parent = parent

        self.colors = colors*(6//len(colors))
        if len(styles) != 0:
            self.styles = styles*(3//len(styles))
        else:
            self.styles = [None]*6
        self.multiple_choice = multiple_choice
        self.use_ind = use_ind
        self.arrow = arrow

    def __repr__(self) -> str:
        return f'Menu:{self.name}'


class ConsoleMenu(object):
    def __init__(self, config: ConfigParser, logger: Logger) -> None:
        self.menu_structure = {
            'init': []
        }
        self.config = config
        self.logger = logger

        # Do log note
        self.logger(f'[{self.__class__.__name__}] has initialized')

    def add_menu(self, menu: Menu) -> None:
        if menu.parent is None:
            menu.parent = 'init'

        self.menu_structure[menu.parent].append(menu)
        self.menu_structure[menu.name] = []
        return None

    def add_menus(self, menus: list[Menu]) -> None:
        for menu in menus:
            self.add_menu(menu)

    def run(self, node: Menu, cache=[]) -> list:
        os.system('cls')
        res = self.get_choice(
            cur_menu=node,
            options=self.menu_structure[node.name],
            use_ind=node.use_ind,
            multiple_choice=node.multiple_choice,
            arrow=node.arrow,
        )
        if len(res) == 0:
            return cache
        if not node.multiple_choice:
            return self.run(res[0], [res[0].name])
        return cache + res

    def get_choice(self, cur_menu: Menu, options: tuple[Menu], use_ind: bool, multiple_choice: bool, arrow: str) -> list:
        cur_line_index = 0
        used = set()
        while True:
            os.system('cls')
            # Print Options
            print(cur_menu.additional_text)
            for i, option in enumerate(options):
                # Line is using
                if i in used:
                    data = termcolor.colored(
                        text=option.name,
                        color=option.colors[0].lower(),
                        on_color='on_' + option.colors[1].lower(),
                        attrs=option.styles[0],
                    )
                # Line isn't using
                else:
                    data = termcolor.colored(
                        text=option.name,
                        color=option.colors[2].lower(),
                        on_color='on_' + option.colors[3].lower(),
                        attrs=option.styles[1],
                    )
                # Line is current
                if i == cur_line_index:
                    data = termcolor.colored(
                        text=option.name,
                        color=option.colors[4].lower(),
                        on_color='on_'+option.colors[5].lower(),
                        attrs=option.styles[2],
                    )
                log = f'[{i}]' if use_ind else f'[{"✅" if i == cur_line_index else "❌"}]'
                if i == cur_line_index:
                    log += arrow
                log += data
                print(log)

            print('\nType <SPACE> to select and <ENTER> to continue...')
            # Get Arrow Input
            while True:
                key = ord(getch())
                if key not in keyboard.keys() or key == 224:
                    continue
                else:
                    key = keyboard[key]
                # go up
                if key in ('W', 'UP_ARROW', 'KP_UP'):
                    cur_line_index = (cur_line_index - 1) if cur_line_index - 1 >= 0 else len(options) - 1

                # go down
                if key in ('S', 'DOWN_ARROW', 'KP_DOWN'):
                    cur_line_index = (cur_line_index + 1) if cur_line_index + 1 <= len(options) - 1 else 0

                # approve input
                if key in ('SPACE',):
                    if multiple_choice:
                        if cur_line_index in used:
                            used.remove(cur_line_index)
                        else:
                            used.add(cur_line_index)
                    else:
                        if cur_line_index in used:
                            used = set()
                        else:
                            used = {cur_line_index}

                # complete choose
                if key in ('ENTER',):
                    result = []
                    if len(options) == 0:
                        return result
                    for i in used:
                        result.append(options[i])
                    return result

                # return
                if key in ('DEL',):
                    return []
                break

    def __repr__(self) -> str:
        return pprint.pformat(self.menu_structure, width=4)




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
