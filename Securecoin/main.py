from core.app import main_page
import flet


flet.app(
    target=main_page,
    name='Securecoin',
    view=flet.AppView.FLET_APP,
    assets_dir='./core/app/assets'
)
