from core.arbitrage import DataParserDaemon
from core.ui import UI
import configparser
import halo


#####################################
config_path = './config.ini'
exchanges = [
    'binance',
    'bybit',
]
tickets = [
    'USDT/BTC',
    'HOT/USDT',
]
#####################################


def main():
    # ---
    # Initialize
    # ---
    config = configparser.ConfigParser()
    config.read(config_path)

    ui = UI(
        config=config,
        system='win'
        )

    parser_daemon = DataParserDaemon(
        exchanges=exchanges,
        tickets=tickets,
    )

    # ---
    # UI Echo
    # ---
    while True:
        ui.clear()
        ui.get_main_menu()
        menu_carrier = ui.get_choice()

        if menu_carrier == '0':
            # stop all daemons
            exit(0)
        elif menu_carrier == '1':
            ui.get_cite_menu()
        elif menu_carrier == '2':
            while True:
                ui.get_server_menu()
                menu_carrier = ui.get_choice()
                if menu_carrier == '0':
                    break
                elif menu_carrier == '1':
                    # ADD PARSER
                    name = input('Name: ')
                    file = input('File: ')
                    parser_daemon.create_daemon(
                        name=name,
                        save_file=file,
                    )
                elif menu_carrier == '2':
                    # REM DAEMON
                    print('REM DAEMON')
                elif menu_carrier == '3':
                    # SEND COMMAND
                    while True:
                        ui.get_send_command_menu()
                        menu_carrier = ui.get_choice()

                        if menu_carrier == '0':
                            break
                        elif menu_carrier == '1':
                            name = input('Name: ')
                            print(parser_daemon.get_daemon_parse_time(name))
                        elif menu_carrier == '2':
                            name = input('Name: ')
                            parser_daemon.stop_daemon(name)
                        elif menu_carrier == '3':
                            name = input('Name: ')
                            parser_daemon.continue_daemon(name)

                elif menu_carrier == '4':
                    print(parser_daemon)


if __name__ == '__main__':
    main()
