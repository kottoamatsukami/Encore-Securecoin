import sqlite3
import configparser

class DataManager(object):
    def __init__(self, config: configparser.ConfigParser) -> None:
        self.config = config

        self.connection = sqlite3.connect(
            database=self.config['Database']['database']
        )
        self.cursor = self.connection.cursor()

        self.__create_table()

    def __create_table(self) -> None:
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_data(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            pseudonym TEXT,
            localisation TEXT,
            deposit REAL,
            started_fiat_banks TEXT,
            finished_fiat_banks TEXT,
            started_exchanges TEXT,
            finished_exchanges TEXT,
            cycle_of TEXT,
            max_bundle_length INTEGER,
            use_only_max_length INTEGER,
            tax REAL,
            transfer_gaz REAL,
            target_spread REAL,
            speed REAL,
            special_tickets TEXT,
            blacklisted_tickets TEXT);
        """)
        self.connection.commit()

    def insert_data(self, data):
        print(data)
        self.cursor.execute(f"""
            INSERT INTO user_data
            (user_id, pseudonym, localisation, deposit,
            started_fiat_banks, finished_fiat_banks,
            started_exchanges, finished_exchanges,
            cycle_of,
            max_bundle_length, use_only_max_length,
            tax, transfer_gaz, target_spread, speed,
            special_tickets, blacklisted_tickets)
            VALUES {data};
        """)
        self.connection.commit()