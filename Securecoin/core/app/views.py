import flet

from .pages.main import Home
from .pages.login import Login


def views_handler(page):
    return {
        '/': flet.View(
            route='/',
            controls=[
                Home(page)
            ],
        ),
        '/login': flet.View(
            route='/login',
            controls=[
                Login(page)
            ],
        )
    }
