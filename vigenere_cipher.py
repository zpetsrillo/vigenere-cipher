from collections import Counter, defaultdict


class vigenere_cipher:
    def __init__(self, train_data, passwd):
        self.train_data = [x.replace(" ", "").upper() for x in train_data]
        self.passwd = passwd.replace(" ", "").upper()

    def converter(self, c, rot):
        # rotate char c through alphabet by rot
        new = ord(c) - rot - ord("A")
        if new < 0:
            new += 26
        new += ord("A")
        return chr(new)

    def convert(self, s, key):
        out = ""

        for i, c in enumerate(s):
            out += self.converter(c, self.numeric_alpha(key[i % len(key)]))

        return out

    def generate_key(self, key_length, train_data):
        full_letter_counts = []
        cipher_key = ""

        # split up train_data based on key length
        for val in train_data:
            position = defaultdict(str)
            letter_counts = []
            for i, c in enumerate(val):
                position[i % key_length] += c

            # find letter frequency
            for k in position:
                letter_count = defaultdict(float)
                counts = Counter(position[k])
                total = float(sum(counts.values()))
                most_common = counts.most_common()
                for letter, count in most_common:
                    letter_count[letter] += count / total * 100
                letter_counts.append(letter_count)

            full_letter_counts.append(letter_counts)

        # determine most common letter based  on frequency accross all train_data
        for i in range(key_length):
            freq_count = defaultdict(float)
            for counts in full_letter_counts:
                for key in counts[i]:
                    freq_count[key] += counts[i][key]
            cipher_key += self.reverse_key(
                sorted(freq_count.items(), key=lambda x: x[1], reverse=True)[0][0]
            )

        return cipher_key

    def reverse_key(self, c):
        # Assuming the most common letter from train_data is 'E' we can deduce the values for the key
        # 'E' is the most common letter of the alphabet
        c = ord(c) - ord("E")
        if c < 0:
            c += 26
        return chr(c + ord("A"))

    def numeric_alpha(self, c):
        # numeric order of letter appearnce in alphabet
        return ord(c) - ord("A")

    def run(self, key_length):
        # return list of all possible solutions for range of 1 to key_length given
        out = []
        for i in range(1, key_length + 1):
            key = self.generate_key(i, self.train_data)
            out.append((len(key), self.convert(self.passwd, key)))

        return out

