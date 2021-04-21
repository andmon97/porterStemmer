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

    """
        CONDITION PART
    """

    # *S - the stem ends with S (and similarly for the other letters).
    def endsWith(self, stem, letter):
        if stem.endswith(letter):
            return True
        else:
            return False


    # *v* - the stem contains a vowel.
    def containsVowel(self, stem):
        for letter in stem:
            if not self.consonant(letter):
                return True
        return False


    # *d - the stem ends with a double consonant (e.g. -TT, -SS).
    def doubleCons(self, stem):
        if len(stem) >= 2:
            if self.isConsonant(stem, -1) and self.isConsonant(stem, -2):
                return True
            else:
                return False
        else:
            return False


    # *o - the stem ends cvc, where the second c is not W, X or Y (e.g. -WIL, -HOP).
    def cvc(self, word):
        if len(word) >= 3:
            lastConsonant = word[-1]
            if self.isConsonant(word, -3) and self.isVowel(word, -2) and self.isConsonant(word, -1):
                if lastConsonant != 'w' and lastConsonant != 'x' and lastConsonant != 'y':
                    return True
                else:
                    return False
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
    # m=2 => TROUBLES, PRIVATE, OATEN, ORRERY.
    def getM(self, word):
        form = self.wordForm(word)
        m = form.count('VC')
        return m