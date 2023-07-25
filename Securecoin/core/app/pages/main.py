import flet


class Home(flet.UserControl):
    def __init__(self, page: flet.Page) -> None:
        super().__init__()
        self.page = page

    def build(self):

        # Navbar

        # main container
        _navbar = flet.Container(
            width=250,
            border_radius=20,
            bgcolor='#383838',
            content=flet.Column(
                height=850,
                controls=[
                    ################################
                    # Product Info
                    ################################

                    flet.Container(
                        content=flet.Image(
                            src='./core/app/assets/icons/loading-animation.png',
                            fit=flet.ImageFit.COVER,
                            scale=0.8
                        ),
                        alignment=flet.alignment.center
                    ),
                    flet.Text(
                            value='Encore Ecosystem Securecoin',
                            style=flet.TextThemeStyle.HEADLINE_SMALL,
                            color='white',
                            text_align=flet.TextAlign.CENTER
                    ),

                    flet.Divider(),
                    ################################
                    # Current Plan
                    ################################


                    ################################
                    # VM Status
                    ################################
                    flet.Container(
                        content=flet.Text(
                            value='Server Status: ST: LC, MS: ok, NON: 1',
                            style=flet.TextThemeStyle.LABEL_MEDIUM,
                            color='white',
                        ),
                        alignment=flet.alignment.center
                    ),
                    flet.Container(
                        content=flet.Text(
                            value='-< Utils >-',
                            style=flet.TextThemeStyle.HEADLINE_MEDIUM,
                            color='white',
                        ),
                        alignment=flet.alignment.center
                    ),
                    ################################
                    # Side Bar Data
                    ################################
                    flet.Container(
                        content=flet.FilledTonalButton(
                            text='CEX Arbitrage',
                            width=200,
                        ),
                        alignment=flet.alignment.center,
                    ),
                    flet.Container(
                        content=flet.FilledTonalButton(
                            text='DEX Arbitrage',
                            width=200,
                        ),
                        alignment=flet.alignment.center,
                    ),
                    flet.Container(
                        content=flet.FilledTonalButton(
                            text='Multi Arbitrage',
                            width=200,
                        ),
                        alignment=flet.alignment.center,
                    ),
                    flet.Container(
                        content=flet.FilledTonalButton(
                            text='Token Checker',
                            width=200,
                        ),
                        alignment=flet.alignment.center,
                    ),
                    flet.Container(
                        content=flet.FilledTonalButton(
                            text='Combo',
                            width=200,
                        ),
                        alignment=flet.alignment.center,
                    ),

                    flet.Container(
                        content=flet.Text(
                            value='-< Bots >-',
                            style=flet.TextThemeStyle.HEADLINE_MEDIUM,
                            color='white',
                        ),
                        alignment=flet.alignment.center
                    ),

                    flet.Container(
                        content=flet.FilledTonalButton(
                            text='Sniper Bot',
                            width=200,
                        ),
                        alignment=flet.alignment.center,
                    ),
                    flet.Container(
                        content=flet.FilledTonalButton(
                            text='Watch Wallets',
                            width=200,
                        ),
                        alignment=flet.alignment.center,
                    ),
                    flet.Container(
                        content=flet.FilledTonalButton(
                            text='Frontrunner',
                            width=200,
                        ),
                        alignment=flet.alignment.center,
                    ),


                ],
                alignment=flet.MainAxisAlignment.CENTER,
                expand=True,

            )
        )
        _result = [
            _navbar,
        ]

        return _result
