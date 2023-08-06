#!/usr/bin/env python
# -*- coding: utf-8 -*-

from importlib.resources import files
from .uheprng import UHEPRNG
from embit import bip39
import argparse

WORDLIST = files("shuffler.wordlists").joinpath("english.txt").read_text().splitlines()


class Shuffler:
    def __init__(self, seed):
        self.seed = seed
        self.prng = UHEPRNG()

        if not self._checksum_seed():
            print("Wrong Seed Checksum")
            raise (ValueError)

        self._init_prng()
        self.shuffled_list = self._shuffle()

    def _init_prng(self):
        self.prng._initState()
        self.prng._hashString(self.seed)

    def _checksum_seed(self):
        """
        Checks if the recovery seed is valid according to bip39 specs
        """
        return bip39.mnemonic_is_valid(self.seed)

    def _shuffle(self):
        """
        Applies Fisher-Yates Algorithm to bip39 wordlist
        """

        lst = WORDLIST
        i = len(lst)
        while i > 0:
            i -= 1
            j = self.prng.random(i + 1)
            lst[i], lst[j] = lst[j], lst[i]

        return lst

    def table(self):
        header = "    ".join([chr(n) for n in range(65, 81)])
        output = ""

        for page in range(2):
            output += f"       {header}\n"
            for line in range(64):
                line_str = ""
                for row in range(16):
                    ix = 64 * 16 * page + 16 * line + row
                    line_str += f"{self.shuffled_list[ix][:4]:5}"

                output += f"{(64*page+line)+1:03} - {line_str}\n"
            output += 85 * "-" + "\n"
            output += f"Seed: {self.seed}\n"
            output += 85 * "-"
            if page == 0:
                output += "\n"

        return output


def main():
    parser = argparse.ArgumentParser(description="BIP39 Shuffler")
    parser.add_argument("--seed", action="store", dest="seed", default=None)

    seed = parser.parse_args().seed

    if seed is not None:
        s = Shuffler(seed=seed)
        print(s.table())
    else:
        print("Please, provide a seed")


if __name__ == "__main__":
    main()
