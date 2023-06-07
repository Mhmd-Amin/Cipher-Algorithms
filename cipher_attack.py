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
