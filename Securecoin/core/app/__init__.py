from .views import views_handler
import flet


async def main_page(page: flet.Page):
    # Connect fonts
    page.fonts = {
        'Astro Space': './core/app/assets/fonts/AstroSpace/AstroSpace.ttf',
        'Do4Brain Bold':    './core/app/assets/fonts/Do4Brain/Do4BrainBold.ttf',
        # ToDO other
    }
    # Favicon
    # await page.add_async(
    #     flet.Image(src='icon.png')
    # )

    page.scroll = "adaptive"
    page.title = 'Securecoin'
    page.bgcolor = '#FFF5EE'
    page.theme_mode = flet.ThemeMode.LIGHT
    page.window_resizable = True
    page.window_full_screen = False  # To do
    page.window_width = 1920
    page.window_height = 1080

    # On resize
    def on_resize(e):
        pass

    def route_change(route):
        page.views.clear()
        page.views.append(
            views_handler(page)[page.route]
        )

    page.on_route_change = route_change

    # Resize
    page.on_resize = on_resize
    await page.go_async('/')
