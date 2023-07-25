from encorelib import cli


class Distributor(object):
    def __init__(self, admin_panel: cli.Menu) -> None:
        # Check realisation of admin panel
        self.__check_panel(admin_panel, 'admin')
        #

        self.admin_panel = admin_panel



    def __check_panel(self, panel: cli.Menu, type_: str) -> None:
        if type_.lower() == 'admin':
            #############
            # ADMIN PANEL
            #############

            # Test 1:
            None

        elif type_.lower() == 'status':
            ##############
            # STATUS PANEL
            ##############
            None
        # TODO: Other panels
        else:
            raise ValueError(f'Unexpected type of panel: {type_}')
