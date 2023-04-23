class Shift:
    def __init__(self, shift: int, mod: int = 26) -> None:
        self.shift = shift
        self.mod = mod

    def encrypt(self, message:str) -> str:
        encrypted_message = ""
        for letter in message:
            if letter.isalpha():
                letter = letter.upper()
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
        a_inverse = self.modular_inverse()
        for letter in cipher_text:
            if letter.isalpha():
                decrypted_message += chr(((ord(letter) - 65 - self.b) * a_inverse) % self.mod + 65)
            else:
                decrypted_message += letter
        return decrypted_message

    def modular_inverse(self) -> int:
        for x in range(1, self.mod):
            if (self.a * x) % self.mod == 1:
                return x
        return None
    
    @staticmethod
    def _has_inverse(a: int, b: int) -> bool:
        while b:
            a, b = b, a % b
        return abs(a) == 1
