class Porter:

    def consonant(self, letter):
        letter = letter.lower()
        if letter == 'a' or letter == 'e' or letter == 'i' or letter == 'o' or letter == 'u':
            return False
        else:
            return True


    def isConsonant(self, word, position):
        letter = word[position]
        letter = letter.lower()
        if self.consonant(letter):
            if letter == 'y' and self.consonant(word[position - 1]):
                return False
            else:
                return True
        else:
            return False


    def isVowel(self, word, i):
        return not(self.isConsonant(word, i))


    # *S - if the stem ends with a particular letter
    def endsWith(self, stem, letter):
        if stem.endswith(letter):
            return True
        else:
            return False


    # *v* - rule that check if there is a vowel in the stem
    def containsVowel(self, stem):
        for letter in stem:
            if not self.consonant(letter):
                return True
        return False


    # *d - rule that check if there is a sequence of double consonants in the stem
    def doubleCons(self, stem):
        if len(stem) >= 2:
            if self.isConsonant(stem, -1) and self.isConsonant(stem, -2):
                return True
            else:
                return False
        else:
            return False


    """
    Every word in the Porter form is [C](VC)^m[V], where
    - [C] possiblie set of Consonants sequence of lenght > 0;
    - (VC)^m sequence of Vowels and Consonants of lenght m;
    - [V] possiblie set of Vowels sequence of lenght > 0.
    """
    # rule that check the word's form
    def wordForm(self, word):
        form = []
        formStr = ''
        for position in range(len(word)):
            if self.isConsonant(word, position):
                if position != 0:
                    previous = form[-1]
                    if previous != 'C':
                        form.append('C')
                else:
                    form.append('C')
            else:
                if position != 0:
                    previous = form[-1]
                    if previous != 'V':
                        form.append('V')
                else:
                    form.append('V')
        for type in form:
            formStr += type
        return formStr


    # obtain the lenght of the (VC) sequence from the form (the m param)
    def getM(self, word):
        form = self.wordForm(word)
        m = form.count('VC')
        return m