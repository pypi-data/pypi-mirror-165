# -*- coding:utf-8 -*-
###
#    Author:         Steven HELLEC
#    Creation Date:  Friday, August 26th 2022, 9:02:05 am
###

from . import *


class GenKeySHException(Exception):

    def __init__(self, raison):
        self.raison = raison

    def __str__(self):
        return self.raison


class GenKeySH:
    """
    Class to generate and store random encryption keys.
    """

    def __init__(self, seed=None):
        self.seed = seed

    def gen_sym_key(self, nb_bytes=32, path_store=None):
        """
        Description :
        -----------
        Generate 16, 24 or 32 bytes key for encryption.
        
        Parameters :
        -----------     
            - nb_bytes (int) : (default : 32) Number of bytes of the keys.
            - path_store (str) : (default : None) Path to the text file which will contains the key.
                       
        Returns :
        ----------
            - key (str) : The key.
        """
        if nb_bytes not in [16, 24, 32]:
            raise GenKeySHException("AES key must be either 16, 24, or 32 bytes long")

        if path_store is not None:
            path, _ = os.path.split(path_store)
            if path != "":
                if not os.path.exists(path):
                    raise GenKeySHException(f"path to store the key is invalid : {path_store}")

        # Initialisation of the seed
        rnd.seed(self.seed)
        key = "".join([rnd.choice(string.hexdigits[:16]) for n in range(nb_bytes)])

        if path_store is not None:
            with open(path_store, "w") as fw:
                fw.writelines(key)

        return key
