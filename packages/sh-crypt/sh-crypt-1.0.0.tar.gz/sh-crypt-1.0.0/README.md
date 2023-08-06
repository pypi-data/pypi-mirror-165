SH Crypt
========
A simple symetric encyption decryption algorithm
------------------------------------------------
About
-----
SH Crypt is base on library cryptography algorithm and use more specifically the Electronic Code Book (ECB) for symetric encryption and decryption.

Here are some code example to use the library.

Generate a key, encrypt and decrypt text
----------------------------------------
```python
from sh_crypt import GenKeySH,CryptSH

key = GenKeySH().gen_sym_key()
# Ex : 'e169344ae15719669ed2fecea1ac4773'

password = "Hello World !!"

crypt = CryptSH(key)

encrypt_password = crypt.encrypt_password(password)
# Ex : '469feb93adc2af609a98e6b7cee859bb'

crypt.decrypt_password(encrypt_password)
# 'Hello World !!'
```

Install
-------
You can install sh-crypt with [pip](https://pypi.org/project/sh-crypt/):

```python
pip install sh-crypt
```

or download the [sh-crypt source](https://github.com/steven1909/sh-crypt/archive/refs/heads/master.zip), unpack it, navigate to the top level directory, and install with the command:

```python
python setup.py install
```