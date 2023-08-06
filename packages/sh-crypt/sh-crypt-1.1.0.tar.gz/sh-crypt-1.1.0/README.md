# SH Crypt

[![PyPI Latest Release](https://img.shields.io/pypi/v/sh-crypt.svg)](https://pypi.org/project/sh-crypt/)
[![License](https://img.shields.io/pypi/l/sh-crypt.svg)](https://github.com/steven1909/sh-crypt/blob/master/LICENSE)
[![codecov](https://codecov.io/gh/steven1909/sh-crypt/branch/master/graph/badge.svg?token=EU0M1RS2NI)](https://codecov.io/gh/steven1909/sh-crypt)
[![CircleCI](https://dl.circleci.com/status-badge/img/gh/steven1909/sh-crypt/tree/master.svg?style=shield)](https://dl.circleci.com/status-badge/redirect/gh/steven1909/sh-crypt/tree/master)

## A simple symetric encyption decryption algorithm
## About

SH Crypt is base on library cryptography algorithm and use more specifically the Electronic Code Book (ECB) for symetric encryption and decryption.

Here are some code example to use the library.

## Generate a key, encrypt and decrypt text

```python
from sh_crypt import GenKeySH, CryptSH
import random as rnd

# Create key generatore
seed = rnd.randint(1, 1e12)
key_gen = GenKeySH(seed)

key = key_gen.gen_sym_key(path_store="mykey.txt")
# Ex : 'e169344ae15719669ed2fecea1ac4773'

password = "Hello World !!"

crypt = CryptSH(key)

encrypt_password = crypt.encrypt_password(password)
# Ex : '469feb93adc2af609a98e6b7cee859bb'

crypt.decrypt_password(encrypt_password)
# 'Hello World !!'
```

As you can see in the example, you can store your generated key in a text file and reuse it later, with the ```path_store``` argument.

## Install
You can install sh-crypt with [pip](https://pypi.org/project/sh-crypt/):

```python
pip install sh-crypt
```

or download the [sh-crypt source](https://github.com/steven1909/sh-crypt/tree/master), choose your version, and install with the command:

```python
python setup.py install
```