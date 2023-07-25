import flet


class Login(flet.UserControl):
    def __init__(self, page: flet.Page) -> None:
        super().__init__()
        self.page = page

    def build(self):
        return flet.Text('This is a login page')
