from typing import List, Dict
import math


class Cryptanalysis:
    def __init__(self):
        pass

    @staticmethod
    def analyze(frequency_dict: dict) -> dict:
        possible_map_list = {
            "single": {
                "E": frequency_dict["single"][0], "T": frequency_dict["single"][1], "A": frequency_dict["single"][2],
                "O": frequency_dict["single"][3], "K": frequency_dict["single"][-5], "J": frequency_dict["single"][-4],
                "X": frequency_dict["single"][-3], "Q": frequency_dict["single"][-2], "Z": frequency_dict["single"][-1]
            },
            "double": {
                "TH": frequency_dict["double"][0], "HE": frequency_dict["double"][1], "IN": frequency_dict["double"][2],
                "ER": frequency_dict["double"][3], "AN": frequency_dict["double"][4], "RE": frequency_dict["double"][5]
            },
            "triple": {
                "THE": frequency_dict["triple"][0], "AND": frequency_dict["triple"][1],
                "ING": frequency_dict["triple"][2], "HER": frequency_dict["triple"][3],
                "HAT": frequency_dict["triple"][4]
            },
            "quadruple": {
                "THAT": frequency_dict["quadruple"][0], "THER": frequency_dict["quadruple"][1],
                "WITH": frequency_dict["quadruple"][2], "TION": frequency_dict["quadruple"][3],
                "HERE": frequency_dict["quadruple"][4]
            }
        }

        return possible_map_list

    @staticmethod
    def sort_frequencies(frequency_dict: dict) -> dict:
        for key in frequency_dict.keys():
            frequency_dict[key] = sorted(frequency_dict[key].items(), key=lambda x: x[1], reverse=True)

        return frequency_dict

    @staticmethod
    def find_frequency(cipher_text: str, frequency_dict: dict = None) -> dict:
        if not frequency_dict:
            frequency = {"single": {}, "double": {}, "triple": {}, "quadruple": {}}
        else:
            frequency = frequency_dict

        if type(cipher_text) == str:
            temp_frequency = Cryptanalysis.__count_frequency(cipher_text)
            for key in frequency.keys():
                for sub_key in temp_frequency[key].keys():
                    frequency[key].update({sub_key: temp_frequency[key].get(sub_key) + frequency[key].get(sub_key, 0)})
        else:
            raise TypeError("Cipher text must be str or list")

        return frequency

    @staticmethod
    def __count_frequency(cipher_text: str) -> dict:
        single_letter = {k: 0 for k in "ABCDEFGHIJKLMNOPQRSTUVWXYZ"}
        double_letter, triple_letter, quadruple_letter = {}, {}, {}
        cipher_text_length = len(cipher_text)

        for i in range(0, cipher_text_length):
            if cipher_text[i].isalpha():
                single_letter[cipher_text[i].upper()] += 1

                if i == cipher_text_length - 1:
                    continue
                key = cipher_text[i].upper() + cipher_text[i + 1].upper()
                double_letter.update({key: double_letter.get(key, 0) + 1})

                if i == cipher_text_length - 2:
                    continue
                key = cipher_text[i].upper() + cipher_text[i + 1].upper() + cipher_text[i + 2].upper()
                triple_letter.update({key: triple_letter.get(key, 0) + 1})

                if i == cipher_text_length - 3:
                    continue
                key = cipher_text[i].upper() + cipher_text[i + 1].upper() + cipher_text[i + 2].upper() + cipher_text[i + 3].upper()
                quadruple_letter.update({key: quadruple_letter.get(key, 0) + 1})

        return {"single": single_letter, "double": double_letter, "triple": triple_letter, "quadruple": quadruple_letter}

    @staticmethod
    def clear_extras(frequency_dict: dict) -> dict:
        remove_dict = {}
        for key in frequency_dict.keys():
            for sub_key in frequency_dict[key].keys():
                for letter in sub_key:
                    if letter.isdigit():
                        if not remove_dict.get(key):
                            remove_dict[key] = []
                        remove_dict[key].append(sub_key)
                        break

        for k, values in remove_dict.items():
            for value in values:
                frequency_dict[k].pop(value)

        return frequency_dict


class PolyAlphabetic:
    def __init__(self, cipher_text: str = None) -> None:
        self.cipher_text = None
        if type(cipher_text) == str:
            self.cipher_text = cipher_text
        else:
            raise (ValueError("Cipher text must be string"))

    # def find_key(self) -> str:
    #     possible_key = ""
    #     return possible_key

    def find_key_length(self) -> List[int]:
        """kasiski_examination"""

        possible_key_length = []
        frequency_dict = Cryptanalysis.sort_frequencies(Cryptanalysis.find_frequency(self.cipher_text))
        selected_word = [frequency_dict["triple"][0][0], frequency_dict["triple"][1][0],
                         frequency_dict["quadruple"][0][0], frequency_dict["quadruple"][1][0]]
        word_gcd = self.__calculate_gcd(self.__calculate_distance(self.__find_positions(selected_word)))

        return possible_key_length

    def __find_positions(self, selected_word: List[str]) -> Dict[str, List[int]]:
        word_position = dict.fromkeys(selected_word, [])
        cipher_text_length = len(self.cipher_text)
        for i in range(cipher_text_length-2):
            triple_letter = self.cipher_text[i].upper() + self.cipher_text[i + 1].upper() + self.cipher_text[i + 2].upper()
            if triple_letter in selected_word:
                word_position[triple_letter].append(i)
            if i == cipher_text_length - 3:
                continue
            quadruple_letter = self.cipher_text[i].upper() + self.cipher_text[i + 1].upper() + self.cipher_text[i + 2].upper() + self.cipher_text[i + 3].upper()
            if quadruple_letter in selected_word:
                word_position[quadruple_letter].append(i)

        return word_position

    @staticmethod
    def __calculate_distance(word_position: Dict[str, List[int]]) -> Dict[str, List[int]]:
        word_distance = {}
        for key, values in word_position.items():
            distance = []
            for i in range(1, len(values)):
                distance.append(values[i] - values[0])
            word_distance[key] = distance
        return word_distance

    @staticmethod
    def __calculate_gcd(words_distance: Dict[str, List[int]]) -> Dict[str, int]:
        word_gcd = {}
        for key, values in words_distance.items():
            values_length = len(values)
            if values_length >= 2:
                word_gcd[key] = math.gcd(values[0], values[1])
            elif values_length == 1:
                word_gcd[key] = values[0]
                continue
            else:
                continue
            for i in range(2, len(values)):
                word_gcd[key] = math.gcd(word_gcd[key], values[i])

        return word_gcd

# TODO: remove repeated pdf part by using generator or Helper class that apply function on all text pages
