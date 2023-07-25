from core.wallet_cracker import Cracker


cracker = Cracker(
    words_path='core/wallet_cracker/english.txt'
)
cracker.run()