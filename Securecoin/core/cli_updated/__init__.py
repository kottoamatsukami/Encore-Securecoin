from configparser import ConfigParser
from msvcrt import getch
import termcolor
import queue
import time
import os


keyboard = {
    119: 'W', 97: 'A', 115: 'S', 100: 'D',
    72: 'UP_ARROW', 80: 'DOWN_ARROW', 75: 'LEFT_ARROW', 77: 'RIGHT_ARROW',
    56: 'KP_UP', 50: 'KP_DOWN', 52: 'KP_LEFT', 54: 'KP_RIGHT',
    13: 'ENTER', 32: 'SPACE', 8: 'BACKSPACE', 83: 'DEL',
}


class MenuElement(object):
    counter = dict()

    def __init__(self, id_=None) -> None:
        if id_ is None:
            self.id = str(len(self.counter))
        else:
            self.id = str(id_)
        self.counter[self.id] = self


class Title(MenuElement):
    def __init__(self, main_text: str, fill_char=' ', hint_1='', char_1=' ', hint_2='', char_2=' ', id_=None) -> None:
        super().__init__(id_=id_)
        self.main_text, self.fill_char = main_text, fill_char
        self.hint_1, self.char_1 = hint_1, char_1
        self.hint_2, self.char_2 = hint_2, char_2

    def print_title(self, width: int, timestamps=0):
        print(self.hint_1.center(width, self.char_1))
        time.sleep(timestamps)
        for line in self.main_text.split('\n'):
            print(line.center(width, self.fill_char), end='')
            time.sleep(timestamps)
        print(self.hint_2.center(width, self.char_2))

    def __repr__(self) -> str:
        return self.main_text


class Option(MenuElement):
    def __init__(self, name: str, id_=None) -> None:
        super().__init__(id_=id_)
        self.name = name

    def __copy__(self):
        return Option(self.name)

    def __repr__(self) -> str:
        return self.name


class Menu(MenuElement):
    def __init__(self, title: Title, name: str, options: tuple, style: ConfigParser, locale: ConfigParser,
                 id_=None) -> None:
        super().__init__(id_=id_)
        self.title = title
        self.name = name
        self.style = style
        self.locale = locale
        self.options = tuple([*options, Option(name=self.locale['Menu']['menu_back_button'])])

    def run(self, width=150):
        return self._get_choice(width)

    def _get_choice(self, width=150):
        cur_line = 0

        while True:
            os.system('cls')
            self.title.print_title(width=width)
            for i, option in enumerate(self.options):
                log = f'[{i}]'\
                    if self.style['Utils']['use_index'].lower() == 'true'\
                    else f'[{self.style["Chars"]["id_selected"] if i == cur_line else self.style["Chars"]["id_not_selected"]}]'

                # Current
                if i == cur_line:
                    data = termcolor.colored(
                        text=log + self.style['Utils']['arrow'] + option.name,
                        color=self.style['Current Selection']['foreground'].lower(),
                        on_color='on_' + self.style['Current Selection']['background'].lower(),
                    )
                # Other
                else:
                    data = termcolor.colored(
                        text=log + option.name,
                        color=self.style['Not Selected']['foreground'].lower(),
                        on_color='on_' + self.style['Not Selected']['background'].lower(),
                    )
                print(data)

            while True:
                key = ord(getch())
                if key not in keyboard.keys() or key == 224:
                    continue
                else:
                    key = keyboard[key]
                # go up
                if key in ('W', 'UP_ARROW', 'KP_UP'):
                    cur_line = (cur_line - 1) if cur_line - 1 >= 0 else len(self.options) - 1

                # go down
                if key in ('S', 'DOWN_ARROW', 'KP_DOWN'):
                    cur_line = (cur_line + 1) if cur_line + 1 <= len(self.options) - 1 else 0

                # complete choose
                if key in ('ENTER',):
                    if self.options[cur_line].name == 'Back':
                        return 'Back'
                    return self.options[cur_line]

                # # return
                # if key in ('DEL',):
                #     return []
                break


class MultiSelectionMenu(MenuElement):
    def __init__(self, title: Title, name: str, options: tuple, style: ConfigParser, locale: ConfigParser,
                 id_=None) -> None:
        super().__init__(id_=id_)
        self.title = title
        self.name = name
        self.style = style
        self.locale = locale
        self.options = tuple([*options, Option(name=self.locale['Menu']['menu_back_button'])])

    def run(self, width=150):
        return self._get_choice(width=width)

    def _get_choice(self, width=150):
        cur_line = 0
        used = set()
        while True:
            os.system('cls')
            self.title.print_title(width=width)
            for i, option in enumerate(self.options):
                log = f'[{i}]'\
                    if self.style['Utils']['use_index'].lower() == 'true'\
                    else f'[{self.style["Chars"]["id_selected"] if i == cur_line else self.style["Chars"]["id_not_selected"]}]'

                # Current
                if i == cur_line:
                    data = termcolor.colored(
                        text=log + self.style['Utils']['arrow'] + option.name,
                        color=self.style['Current Selection']['foreground'].lower(),
                        on_color='on_' + self.style['Current Selection']['background'].lower(),
                    )
                else:
                    # Selected
                    if i in used:
                        data = termcolor.colored(
                            text=log  + option.name,
                            color=self.style['Selected']['foreground'].lower(),
                            on_color='on_' + self.style['Selected']['background'].lower(),
                        )
                    # Not Selected
                    else:
                        data = termcolor.colored(
                            text=log + option.name,
                            color=self.style['Not Selected']['foreground'].lower(),
                            on_color='on_' + self.style['Not Selected']['background'].lower(),
                        )
                print(data)

            while True:
                key = ord(getch())
                if key not in keyboard.keys() or key == 224:
                    continue
                else:
                    key = keyboard[key]
                # go up
                if key in ('W', 'UP_ARROW', 'KP_UP'):
                    cur_line = (cur_line - 1) if cur_line - 1 >= 0 else len(self.options) - 1

                # go down
                if key in ('S', 'DOWN_ARROW', 'KP_DOWN'):
                    cur_line = (cur_line + 1) if cur_line + 1 <= len(self.options) - 1 else 0

                # complete choose
                if key in ('ENTER',):
                    if self.options[cur_line].name == 'Back':
                        return 'Back'
                    res = []
                    for index in used:
                        res.append(index)
                    return res

                # # return
                # if key in ('DEL',):
                #     return []
                break


class MenuAgregator(object):
    def __init__(self, root) -> None:
        self.root = root
        self.queue = queue.Queue()

    def run(self, width=150):
        self.queue.put(self.root)
        while self.queue.qsize() > 0:
            lst = self.queue.get()
            if isinstance(lst, Menu or Option or MultiSelectionMenu):
                nxt = lst.run(width=width)
            else:
                if lst == 'Back':
                    continue
                else:
                    return lst
            self.queue.put(lst)
            self.queue.put(nxt)
