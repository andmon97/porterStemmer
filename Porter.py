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

    # replace the removePart with the replacePart in the word
    def replace(self, word, removePart, replacePart):
        position = word.rfind(removePart)
        base = word[:position]
        replaced = base + replacePart
        return replaced

    # replace the removePart with the replacePart in the word if M is > 0
    def replaceM0(self, word, removePart, replacePart):
        position = word.rfind(removePart)
        base = word[:position]
        if self.getM(base) > 0:
            replaced = base + replacePart
            return replaced
        else:
            return word

    # replace the removePart with the replacePart in the word if M is > 1
    def replaceM1(self, word, removePart, replacePart):
        position = word.rfind(removePart)
        base = word[:position]
        if self.getM(base) > 1:
            replaced = base + replacePart
            return replaced
        else:
            return word


    """
        STEP 1a:
        - SSES -> SS (Example : caresses -> caress)
        - IES -> I (Example : ponies -> poni ; ties -> ti)
        - SS -> SS (Example : caress -> caress)
        - S -> (Example : cats -> cat)
    """
    def step1a(self, word):
        if word.endswith('sses'):
            word = self.replace(word, 'sses', 'ss')
        elif word.endswith('ies'):
            word = self.replace(word, 'ies', 'i')
        elif word.endswith('ss'):
            word = self.replace(word, 'ss', 'ss')
        elif word.endswith('s'):
            word = self.replace(word, 's', '')
        return word

    """
        STEP 1b:
    - (m>0) EED -> EE (Example : feed -> feed ; agreed -> agree)
    - (v) ED -> (Example : plastered -> plaster ; bled -> bled)
    - (v) ING -> (Example : motoring -> motor ; sing -> sing)
    - S -> (Example : cats -> cat)
    If the second or third of the rules in Step 1b is successful, the following is done:
    - AT -> ATE (Example : conflat(ed) -> conflate)
    - BL -> BLE (Example : troubl(ed) -> trouble)
    - IZ -> IZE (Example : siz(ed) -> size)
    - S -> (Example : cats -> cat)
    - (*d and not (*L or *S or *Z)) -> single letter (Example : hopp(ing) -> hop ; tann(ed) -> tan ; fall(ing) -> fall ;
     hiss(ing) -> hiss ; fizz(ed) -> fizz)
    - (m=1 and *o) -> E (Example : fail(ing) -> fail ; fil(ing) -> file)

    The rule to map to a single letter causes the removal of one of the double letter pair. The -E is put back on -AT, 
    -BL and -IZ, so that the suffixes -ATE, -BLE and -IZE can be recognised later. This E may be removed in step 4.
    """
    def step1b(self, word):
        optionalStep = False
        if word.endswith('eed'):
            position = word.rfind('eed')
            base = word[:position]
            word = self.replaceM0(base, 'eed', 'ee')
        elif word.endswith('ed'):
            position = word.rfind('ed')
            base = word[:position]
            if self.containsVowel(base):
                word = base #truncate the part ed
                optionalStep = True     # the optional step will be executed
        elif word.endswith('ing'):
            position = word.rfind('ing')
            base = word[:position]
            if self.containsVowel(base):
                word = base #truncate the part ed
                optionalStep = True     # the optional step will be executed
        if optionalStep:
            if word.endswith('at') or word.endswith('bl') or word.endswith('iz'):
                word += 'e'
            elif self.doubleCons(word) and not self.endsWith(word, 'l') and not self.endsWith(word, 's') and not self.endsWith('z'):
                word = word[:-1]
            elif self.getM(word) == 1 and self.cvc(word):
                word += 'e'
        return word


    """
        STEP 1c:
    - (\*v\*) Y -> I (Example : happy -> happi ; sky -> sky)
    """
    def step1c(self, word):
        if word.endswith('y'):
            position = word.rfind('y')
            base = word[:position]
            if self.containsVowel(base):
                word = base
                word += 'i'
        return word