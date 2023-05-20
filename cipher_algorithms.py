from math import sqrt
import numpy as np

class Shift:
    def __init__(self, shift: int, mod: int = 26) -> None:
        self.shift = shift
        self.mod = mod

    def encrypt(self, message:str) -> str:
        encrypted_message = ""
        for letter in message.upper():
            if letter.isalpha():
                encrypted_message += (chr((ord(letter) - 65 + self.shift) % self.mod + 65))
            else:
                encrypted_message += letter
        return encrypted_message

    def decrypt(self, cipher_text: str) -> str:
        decrypted_message = ""
        for letter in cipher_text:
            if letter.isalpha():
                decrypted_message += (chr((ord(letter) - 65 - self.shift) % self.mod + 65))                
            else:
                decrypted_message += letter
        return decrypted_message


class Affine:
    def __init__(self, a: int, b: int, mod: int = 26) -> None:
        if Affine._has_inverse(a, mod):
            self.a = a
            self.b = b
            self.mod = mod
        else:
            raise(ValueError("{a} hasn`t inverse in mod{mod}"))
        
    def encrypt(self, message: str) -> str:
        encrypted_message = ""
        for letter in message.upper():
            if letter.isalpha():
                letter = (ord(letter) -65) * self.a
                encrypted_message += chr((letter + self.b) % self.mod + 65)
            else:
                encrypted_message += letter
        return encrypted_message

    def decrypt(self, cipher_text: str) -> str:
        decrypted_message = ""
        a_inverse = self.modular_inverse(self.a, self.mod)
        for letter in cipher_text.upper():
            if letter.isalpha():
                decrypted_message += chr(((ord(letter) - 65 - self.b) * a_inverse) % self.mod + 65)
            else:
                decrypted_message += letter
        return decrypted_message

    @staticmethod
    def modular_inverse(a:int, mod: int) -> int:
        for x in range(1, mod):
            if (a * x) % mod == 1:
                return x
        return None
    
    @staticmethod
    def _has_inverse(a: int, b: int) -> bool:
        while b:
            a, b = b, a % b
        return abs(a) == 1


class Playfair:
    def __init__(self, key: str) -> None:
        alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ"
        self.table = []

        key = key.upper()
        for i in range(len(key)):
            if key[i] == 'J':
                key[i] = 'I'

        temp_table = "".join(dict.fromkeys(key+alphabet))
        self.table = Playfair._slice_str(temp_table, 0, 25, 5)

    def encrypt(self, message: str) -> str:
        encrypted_message = ""
        message = list(map(str, message.upper()))

        i = 0
        while i < len(message):
            if not message[i].isalpha():
                message.pop(i)
            i += 1

        i = 0
        while i < len(message):
            if len(message) - i == 1:
                message.append('X')
            if message[i] == message[i+1]:
                message.insert(i, 'X')
            i += 2

        pair_letter_list = self._slice_str(''.join(message), 0, len(message), 2)
        for letters in pair_letter_list:
            pos = self._letters_position(letters)
            if pos[0][0] == pos[1][0]:
                encrypted_message += self.table[pos[0][0]][(pos[0][1]+1) % 5]
                encrypted_message += self.table[pos[1][0]][(pos[1][1]+1) % 5]
            elif pos[0][1] == pos[1][1]:
                encrypted_message += self.table[(pos[0][0]+1) % 5][pos[0][1]]
                encrypted_message += self.table[(pos[1][0]+1) % 5][pos[1][1]]
            else:
                encrypted_message += self.table[pos[0][0]][pos[1][1]]
                encrypted_message += self.table[pos[1][0]][pos[0][1]]

        return encrypted_message
    
    def decrypt(self, cipher_text: str) -> str:
        decrypted_message = ""

        cipher_text = cipher_text.upper()
        pair_letter_list = self._slice_str(''.join(cipher_text), 0, len(cipher_text), 2)
        for letters in pair_letter_list:
            pos = self._letters_position(letters)
            if pos[0][0] == pos[1][0]:
                decrypted_message += self.table[pos[0][0]][(pos[0][1]-1) % 5]
                decrypted_message += self.table[pos[1][0]][(pos[1][1]-1) % 5]
            elif pos[0][1] == pos[1][1]:
                decrypted_message += self.table[(pos[0][0]-1) % 5][pos[0][1]]
                decrypted_message += self.table[(pos[1][0]-1) % 5][pos[1][1]]
            else:
                decrypted_message += self.table[pos[0][0]][pos[1][1]]
                decrypted_message += self.table[pos[1][0]][pos[0][1]]

        return decrypted_message

    @staticmethod
    def _slice_str(text: str, start: int, end: int, step: int) -> list:
        sliced_list = []
        for i in range(start, end, step):
            x = i
            sliced_list.append(list(map(str, text[x:x+step]))) 
        return sliced_list

    def _letters_position(self, letters: list) -> tuple:
        pos = []

        for letter in letters:
            found = False
            if letter == 'J':
                letter = 'I'
            
            i = 0
            while i < 5 and not found:
                j = 0
                while j < 5 and not found:
                    if letter == self.table[i][j]:
                        found = True
                        pos.append([i, j])
                    j += 1
                i += 1

        return pos
    

class Hill:
    def __init__(self, key: str) -> None:
        self.set_key(key)

    def encrypt(self, message:str) -> str:
        if len(message) != len(self._key):
            raise(ValueError("The length of key must equal to the length of message to the power of 2"))

        return self.multiply(message, self._key)

    def decrypt(self, cipher_text: str) -> str:
        if len(cipher_text) != len(self._key):
            raise(ValueError("The length of key must equal to the length of cipher text to the power of 2"))
        
        det = int(np.linalg.det(self._key))
        if det == 0 or not Affine._has_inverse(det, 26):
            raise("The key has not inverse")    
        inv_det = Affine.modular_inverse(det, 26)
        cofactor = np.linalg.inv(self._key).T * det
        inverse_matrix = np.remainder((inv_det * cofactor), 26).T
        return self.multiply(cipher_text, inverse_matrix)

    @staticmethod
    def multiply(text: str, key: np.ndarray) -> str:
        text = list(map(lambda x: ord(x)-65, text.upper()))
        text = np.reshape(text, (len(text), 1))
        ans = np.matmul(key, text)
        ans = np.remainder(np.rint(ans), 26) + 65
        ans = "".join(map(lambda x: chr(int(x)), ans.reshape(-1).tolist()))
        return ans

    def set_key(self, key: str) -> None:
        msg_length = sqrt(len(key))
        if msg_length % 1 != 0:
            raise("The key length must be square number")
        key = list(map(lambda x: ord(x)-65, key.upper()))
        self._key = np.reshape(key, (int(msg_length), int(msg_length)))


class Vigenere:
    def __init__(self, key: str) -> None:
        self.key = key.upper()

    def encrypt(self, message: str) -> str:
        encrypted_message = ""
        key_length = len(self.key)
        i = 0
        for letter in message.upper():
            if letter.isalpha():
                encrypted_message += chr(((ord(letter) - 65) + (ord(self.key[i]) - 65)) % 26 + 65)
                i += 1
                if i == key_length:
                    i = 0
            else:
                encrypted_message += letter

        return encrypted_message
    
    def decrypt(self, cipher_text: str) -> str:
        decrypted_message = ""
        key_length = len(self.key)
        i = 0
        for letter in cipher_text.upper():
            if letter.isalpha():
                decrypted_message += chr(((ord(letter) - 65) - (ord(self.key[i]) - 65) + 26) % 26 + 65)
                i += 1
                if i == key_length:
                    i = 0
            else:
                encrypted_message += letter

        return decrypted_message
