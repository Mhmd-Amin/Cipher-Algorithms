class Shift:
    def __init__(self, shift: int, mod: int = 26) -> None:
        self.shift = shift
        self.mod = mod

    def encrypte(self, message:str) -> str:
        encrypted_message = ""
        for letter in message:
            if letter.isalpha():
                letter = letter.upper()
                encrypted_message += (chr((ord(letter) - 65 + self.shift) % self.mod + 65))
            else:
                encrypted_message += letter
        return encrypted_message

    def decrypte(self, message: str) -> str:
        decrypted_message = ""
        for letter in message:
            if letter.isalpha():
                decrypted_message += (chr((ord(letter) - 65 - self.shift) % self.mod + 65))                
            else:
                decrypted_message += letter
        return decrypted_message
