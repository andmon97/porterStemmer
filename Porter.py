class Porter:

    def isNotConsonant(self, letter):
        letter = letter.lower()
        if letter == 'a' or letter == 'e' or letter == 'i' or letter == 'o' or letter == 'u':
            return False
        else:
            return True


    def isConsonant(self, word, i):
        letter = word[i]
        letter = letter.lower()
        if self.isNotConsonant(letter):
            if letter == 'y' and self.isNotConsonant(word[i-1]):
                return False
            else:
                return True
        else:
            return False


    def isVowel(self, word, i):
        return not(self.isConsonant(word, i))


