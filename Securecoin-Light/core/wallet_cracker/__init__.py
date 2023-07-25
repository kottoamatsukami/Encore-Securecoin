from time import sleep
import requests
import bitcoinlib
import os
import hashlib
from datetime import timedelta, datetime

colour_cyan = '\033[36m'
colour_reset = '\033[0;0;39m'
colour_red = '\033[31m'
colour_green = '\033[0;32m'
colour_yellow = '\033[0;33m'
colour_purple = '\033[0;35m'

const = "m/44'/00'/0'/0/"


class Cracker(object):
    def __init__(self, words_path: str) -> None:
        assert os.path.exists(words_path), 'Unavailable words path ' + words_path
        with open(words_path, 'r') as f:
            self.words = f.read().split('\n')

    @staticmethod
    def seconds_to_str(elapsed=None):
        if elapsed is None:
            return datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
        else:
            return str(timedelta(seconds=elapsed))


    def log(self, txt, elapsed=None):
        print('\n ' + colour_cyan + '  [TIMING]> [' + self.seconds_to_str() + '] ----> ' + txt + '\n' + colour_reset)
        if elapsed:
            print("\n " + colour_red + " [TIMING]> Elapsed time ==> " + elapsed + "\n" + colour_reset)


    def create_valid_mnemonics(self, strength=128):
        rbytes = os.urandom(strength // 8)
        h = hashlib.sha256(rbytes).hexdigest()
        b = (bin(int.from_bytes(rbytes, byteorder="big"))[2:].zfill(len(rbytes) * 8) + bin(int(h, 16))[2:].zfill(256)[: len(rbytes) * 8 // 32])
        result = []
        for i in range(len(b) // 11):
            idx = int(b[i * 11: (i + 1) * 11], 2)
            result.append(self.words[idx])
        return " ".join(result)

    @staticmethod
    def mnem_to_seed(words):
        salt = 'mnemonic'
        seed = hashlib.pbkdf2_hmac("sha512", words.encode("utf-8"), salt.encode("utf-8"), 2048)
        return seed

    @staticmethod
    def seed_to_private_key(seed, flag):
        b = bitcoinlib.keys.HDKey.from_seed(seed)
        return b.subkey_for_path(const + flag).address()

    def run(self):
        self.log("Start Program")
        print("List loading, Good Luck...")
        query = []
        count = 0
        total = 0
        while True:
            line = self.create_valid_mnemonics()
            seed = self.mnem_to_seed(line)
            adders = {
                f'addr{i}': self.seed_to_private_key(seed, str(i)) for i in range(128)
            }


            query = list(adders.values())
            request = requests.get("https://blockchain.info/multiaddr?active=%s" % ','.join(query), timeout=10)
            request = request.json()
            print(colour_green + '\nWords for Wallet import : ' + colour_yellow + line + colour_reset)
            print(colour_green + "\nScan Number" + ' : ' + colour_reset + str(count) + ' : ' + colour_green + "Total Wallets Checked" + ' : ' + colour_reset + str(total))
            print(colour_red   + ' <======================== Bitcoin Addresses Checked for Final Balance / Total Received / Total Sent==================>' + '\n' + colour_reset)
            for row in request["addresses"]:
                print(row)
                if row["total_received"] > 0 or row["final_balance"] > 0:  # final_balance or n_tx or total_received or total_sent
                    print(colour_purple + ' <================================= WINNER WINNER WINNER =================================>' + '\n' + colour_reset)
                    print(colour_green  + ' <====== WINNER WINNER WINNER ================================= WINNER WINNER WINNER ======>' + '\n' + colour_reset)
                    print(colour_yellow + "mnemonics ==== Found!!!\n mnemonics : " + line + colour_reset)
                    print(colour_purple + ' <================================= WINNER WINNER WINNER =================================>' + '\n' + colour_reset)
                    print(colour_green  + ' <====== WINNER WINNER WINNER ================================= WINNER WINNER WINNER ======>' + '\n' + colour_reset)

                    f = open(u"winner.txt", "a")
                    f.write('\n mnemonics: ' + line)
                    f.write('\n<======= Bitcoin Addresses Checked for Final Balance / Total Received / Total Sent=======>')

                    for i, adder in enumerate(adders):
                        f.write(f'\n {const} {i}    BTC Address: {adders[adder]}')

                    f.write('\n<======= Bitcoin Addresses Checked for Final Balance / Total Received / Total Sent=======>')
                    f.close()
                    break

            # Reset counter
            query = []
