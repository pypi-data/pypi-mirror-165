# -*- coding:utf-8 -*-
###
#    Author:         Steven HELLEC
#    Creation Date:  Thursday, August 25th 2022, 7:22:53 pm
###

from . import *


class CryptSHException(Exception):

    def __init__(self, raison):
        self.raison = raison

    def __str__(self):
        return self.raison


class CryptSH:
    """
    Class to encrypt and decrypt with symetric key strings.
    """

    def __init__(self, key):
        """
        Setting of object attributes.
        """
        if not isinstance(key, str):
            raise CryptSHException(f"key must be string : {type(key)}")

        if not all(c in string.hexdigits for c in key):
            raise CryptSHException(f"Non-hexadecimal number found in key : {key}")

        key = bytes.fromhex(key)

        if len(key) not in [16, 24, 32]:
            raise CryptSHException(f"key must have len equal to 16, 24 or 32 : {len(key)}")

        self.cipher = Cipher(algorithms.AES(key), modes.ECB())
        self.padder = padding.PKCS7(algorithms.AES(key).block_size)

    def encrypt_password(self, password):
        """
        Description :
        -----------
        Encrypt the provided password.

        Parameters :
        -----------
            - password (str) : String to encrypt.
            - key (str) : Encrypted key.

        Returns :
        ----------
            - _ (str) : Encrypted password.
        """
        if not isinstance(password, str):
            raise CryptSHException(f"password must be string : {type(password)}")

        password_bytes = self.__pad(bytes(password, encoding="utf8"))
        return binascii.hexlify(self.cipher.encryptor().update(password_bytes)).decode("utf8")

    def decrypt_password(self, password_encrypt):
        """
        Description :
        -----------
        Decrypt an encrypted password with a provided key

        Parameters :
        -----------
            - password_encrypt (str) : Encrypted string.
            - key (str) : Decrypting key.

        Returns :
        ----------
            - _ (str) : String decrypted.
        """
        if not isinstance(password_encrypt, str):
            raise CryptSHException(f"password_encrypt must be string : {type(password_encrypt)}")

        enc = bytes.fromhex(password_encrypt)
        return self.__unpad(self.cipher.decryptor().update(enc)).decode("utf8")

    def __unpad(self, s):
        """
        Description :
        -----------
        Unpad string to match with the len size of AES.

        Parameters :
        -----------
            - s (bytes) : Sequence of blocs.

        Returns :
        ----------
            - _ (str) : list of characters.
        """
        unpadder = self.padder.unpadder()
        return unpadder.update(s) + unpadder.finalize()

    def __pad(self, s):
        """
        Description :
        -----------
        Transforms a sequence of bytes into a multiple of blocks of the useful size for AES

        Parameters :
        -----------
            - s (str) : List of bytes.
        Returns :
        ----------
            - _ (bytes) : Sequence of blocs.
        """
        padder = self.padder.padder()
        return padder.update(s) + padder.finalize()
