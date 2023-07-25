from encorelib import cli
from encorelib.cli import logo
from core.cli import text
from configparser import ConfigParser


config = ConfigParser()
localisation = ConfigParser()

config.read('./settings/settings.ini')
localisation.read(config['general']['language'])


STYLE_classic = ConfigParser()
STYLE_premium = ConfigParser()
STYLE_hack = ConfigParser()
STYLE_red = ConfigParser()

STYLE_classic.read('./settings/colorscheme/classic')
STYLE_premium.read('./settings/colorscheme/premium')
STYLE_hack.read('./settings/colorscheme/hack')
STYLE_red.read('./settings/colorscheme/red')


if config['terminal']['show_logo'].lower() == 'true':
    logo.greeting(
        logo=text.logo,
        product=text.product,
        version='0.0.1',
        rows=int(config['terminal']['height']),
        cols=int(config['terminal']['width']),
        delay_1=0.75, delay_2=0.1, delay_3=0.5,
    )

main_menu = cli.Menu(
    cli.Text(
        text='< Securecoin >',
        colorscheme=STYLE_premium,
        fill_char='-',
    ),
    cli.Text(
        text=text.menu,
        colorscheme=STYLE_premium,
    ),
    cli.Text(
        text='< Choose one option below >',
        colorscheme=STYLE_premium,
        fill_char='-',
    ),
    cli.Keypad(
        cli.Selection(
            placeholder=[
                cli.Button(text=localisation['CLI']['cex_dex_arbitrage_menu'], colorscheme=STYLE_premium),
                cli.Button(text=localisation['CLI']['cex_arbitrage_menu'],     colorscheme=STYLE_premium),
                cli.Button(text=localisation['CLI']['dex_arbitrage_menu'],     colorscheme=STYLE_premium),
                cli.Button(text=localisation['CLI']['sniper_bot_menu'],        colorscheme=STYLE_premium),
                cli.Button(text=localisation['CLI']['frontrunner_bot_menu'],   colorscheme=STYLE_premium),
                cli.Button(text=localisation['CLI']['whale_trading_bot_menu'], colorscheme=STYLE_premium),
                cli.Button(text=localisation['CLI']['watch_wallet_bot_menu'],  colorscheme=STYLE_premium),
            ],
        ),
        cli.Selection(
            placeholder=[
                [
                    cli.BackButton(text=localisation['CLI']['exit_button_text'], colorscheme=STYLE_premium),
                    cli.ConfirmButton(text=localisation['CLI']['confirm_button_text'], colorscheme=STYLE_premium),
                ]
            ]
        ),
    ),

    width=int(config['terminal']['width']), length=int(config['terminal']['height']), colorscheme=STYLE_premium,
)
