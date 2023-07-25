from core.cli import logo
from core import cli
import configparser
import text

################################
# P A R A M E T E R S
################################
cols, rows = 150, 50
style = 'core/cli/colors/colorscheme (Premium).ini'
skip_intro = True
################################


colorscheme = configparser.ConfigParser()
colorscheme.read(style)

securecoin_main_menu = cli.Menu(
    cli.Text(
        text='< Securecoin >',
        colorscheme=colorscheme,
        fill_char='-'
    ),
    cli.Text(
        text=text.menu,
        colorscheme=colorscheme,
    ),
    cli.Text(
        text='<[ Choose 1 option below ]>',
        colorscheme=colorscheme,
        fill_char='-'
    ),
    cli.Keypad(
        cli.Selection(
            placeholder=[
                cli.Button(text='CEX|DEX Arbitrage', colorscheme=colorscheme, alignment='center'),
                cli.Button(text='CEX Arbitrage',     colorscheme=colorscheme, alignment='center'),
                cli.Button(text='DEX Arbitrage',     colorscheme=colorscheme, alignment='center'),
                cli.Button(text='Watch Wallets Bot', colorscheme=colorscheme, alignment='center'),
                cli.Button(text='Whale Trading',     colorscheme=colorscheme, alignment='center'),
            ],
        ),
    ),
    cli.Keypad(
        cli.Selection(
            placeholder=[
                [
                    cli.BackButton(text='Back', colorscheme=colorscheme,       alignment='center', padding=+10),
                    cli.ConfirmButton(text='Confirm', colorscheme=colorscheme, alignment='center', padding=-10),
                ]
            ]
        )
    ),
    width=cols,
    length=rows,
    colorscheme=colorscheme,
)


#############
# S T A R T
#############
cli.prepare_terminal(
    background_color=colorscheme['terminal']['background'],
    foreground_color=colorscheme['terminal']['foreground'],
)

if not skip_intro:
    logo.greeting(
        logo=text.logo,
        product=text.product,
        version='Preview-1',
        cols=cols,
        rows=rows,
        delay_1=0.2,
        delay_2=0.1,
        delay_3=0.5,
    )

while True:
    result = securecoin_main_menu.run()
    #print(result)
    break
cli.prepare_terminal(
    background_color='black',
    foreground_color='white',
)
