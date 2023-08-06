# BIP39 Seed Shuffler
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

This project is inspired in the awesome tool [borderwallets](https://www.borderwallets.com/),
and the goal is to provide a simple linux commandline tool that serves as a double
check of the generated grid.

This project is intended for educational purposes and is not meant to be used on
any computer or device connected to the internet.

## Installation:

```
python -m pip install seed-shuffler
```

or, via the git repo:
```
git clone https://github.com/amarjen/seed-shuffler.git
cd seed-shuffler
python -m pip install .
```

## Usage:
:biohazard: Remember not to write any real seed linked to actual funds,
unless it is on a trusted airgap computer and you know what you are doing.
:warning: Don't Trust, Verify

```
seedshuffler --seed="own ginger excuse humble abstract always remain math solar jealous craft coach"
```

In order to generate a nice printable PDF from the text output we can use the legendary tools `enscript` and `ps2pdf`, eg:
```
export SEED="own ginger excuse humble abstract always remain math solar jealous craft coach"
seedshuffler --seed="${SEED}" > grid.txt
enscript -2r -f Courier7 -F Courier7 -j grid.txt -o grid.ps
ps2pdf grid.ps
# clean files
rm grid.pdf grid.ps grid.txt
```

![image](./grid.jpg)

## External dependencies:
- [Embit](https://www.embit.rocks) is only used to validate a bip39 seed by computing its checksum.
- The repo includes the module [uheprng.py](https://github.com/wuftymerguftyguff/uheprng) a python implementation of the Ultra High Entropy Pseudo Random Number Generator developed by
Steve Gibson of grc.com. This is the PRNG that the tool uses to deterministically generate a grid from a bip39 seed.
