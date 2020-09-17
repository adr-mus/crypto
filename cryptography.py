import numpy as np
from numth.modular import det, mat_inverse
from numth import divisors

ABC = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
ABC_INV =  {ABC[i]: i for i in range(26)}

class CaesarCipher:
    """ Represents the Ceasar cipher. """
    def __init__(self, shift: int):
        self.shift = shift % 26
    
    def cipher(self, text: str):
        nums = np.array([ABC_INV[letter] for letter in text.upper() if not letter.isspace()])
        shifted = (nums + self.shift) % 26
        return "".join(ABC[num] for num in shifted)

    def decipher(self, text: str):
        nums = np.array([ABC_INV[letter] for letter in text.upper() if not letter.isspace()])
        shifted = (nums - self.shift) % 26
        return "".join(ABC[num] for num in shifted)
    
    @classmethod
    def crack(cls, m: str, c: str):
        """ Attempts to recreate the shift based on the message m and
            its encryption c. """
        shift = (ABC_INV[c[0]] - ABC_INV[m[0]]) % 26
        if any((ABC_INV[c[i]] - ABC_INV[m[i]]) % 26 != shift for i in range(1, len(m))):
            raise ValueError("Contradiction.")
        return cls(shift)


class TranspositionCipher:
    """ Represents transposition cipher. """
    def __init__(self, line_len: int):
        self.line_len = line_len
    
    def cipher(self, text: str):
        text = np.reshape(list(text), (-1, self.line_len))
        return "".join(str(letter) for letter in np.ravel(text.T))
    
    decipher = cipher

    @classmethod
    def crack(cls, e: str):
        """ Loops over all possible transpositions of the encrypted
            text e. It's up to the user to decide when the cipher is
            broken - then type any character and press enter. """ 
        for line_len in divisors(len(e)):
            cipher = cls(line_len)
            if input(cipher.cipher(e)):
                break
        else:
            raise ValueError("Possibilities exhausted.")
        return cipher


    

class HillCipher:
    """ Represents the Hill cipher. 
        k1 - the matrix part of the key
        k2 - the vector part of the key
        p - modulus """

    def __init__(self, k1: "numpy array", k2: "numpy array", p: int):
        self.k1 = k1 % p
        self._k1_inv = mat_inverse(self.k1, p)
        self.k2 = k2 % p
        self.p = p

    def cipher(self, m: "iterable of ints"):
        m = np.reshape(m, (self.k1.shape[0], -1), "F")
        return np.ravel((self.k1.dot(m) + self.k2) % self.p, "F")

    def decipher(self, c: "iterable of ints"):
        """ Deciphers the message c given as an iterable of ints. """
        c = np.reshape(c, (self.k1.shape[0], -1), order="F")
        m = self._k1_inv.dot(c - self.k2) % self.p
        return np.ravel(m, order="F")

    @classmethod
    def crack(cls, m: "iterable of ints", c: "iterable of ints", p: int):
        """ Attempts to recreate the key based on the message m and
            its encryption c assuming the modulus is p. """
        sizes = (d for d in divisors(len(m)) if d ** 2 + d <= len(m))
        for size in sizes:
            M = np.reshape(m, (size, -1), order="F")
            C = np.reshape(c, (size, -1), order="F")
            m0, c0 = M[:, [0]], C[:, [0]]
            vecs = (M - m0) % p
            vals = (C - c0) % p

            start = 1
            P = vecs[:, start : (start + size)]
            while det(P, p) == 0:
                start += 1
                P = vecs[:, start : (start + size)]
            P_inv = mat_inverse(P, p)

            corr_vals = vals[:, start : (start + size)]
            K1 = corr_vals.dot(P_inv) % p
            K2 = (c0 - K1.dot(m0)) % p

            if ((K1.dot(M) + K2) % p == C).all():
                return cls(K1, K2, p)

        raise ValueError("Not enough information.")
