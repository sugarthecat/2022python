import random as r

class Culture:
    def __init__(self):
        self.consonants = "strdmnc"
        self.citynames = {}
        self.vowels = "aeio"
        for i in range(8):
            self.consonants += r.choice("rtpsdfghklcvbnm" + self.consonants)
        for i in range(9):
            self.vowels += r.choice("aeio" + self.vowels)
        self.consonants += r.choice("zxwj")
        self.vowels += r.choice("yu")
        suffixes = ["ang","burg","fort","an","oto","aka", " City", " Town", "grad","ton","port","dam", "ai","wood","borough",'pol','ham',"sk",'stadt','ia']
        self.suffixes = [r.choice(suffixes),r.choice(suffixes)]
        
        self.ethnicname = r.choice([r.choice(self.consonants) + r.choice(self.consonants) + r.choice(self.vowels) + r.choice(self.consonants),
                                    r.choice(self.consonants) + r.choice(self.vowels) + r.choice(self.vowels) + r.choice(self.consonants),
                                    #r.choice(self.consonants) + r.choice(self.vowels) + r.choice(self.consonants) + r.choice(self.consonants),
                                    #r.choice(self.vowels) + r.choice(self.consonants) + r.choice(self.vowels) + r.choice(self.consonants),
                                    ]
                                   )

        addtree = [
            ["lbdwpbsrgk","ian"],
            ["dnt","ch"],
            ["mtwnljd","ish"],
            ["cmrz","an"],
            ["tpzh","ine"],
            ["lnfg","ean"],
            ["tglvdxzsk","ite"]
            ]
        possads = []
        for poss in addtree:
            if self.ethnicname[3] in poss[0]:
                possads.append(poss[1])
        if len(possads) == 0:
            self.ethnicity = self.ethnicname
        else:
            self.ethnicity = self.ethnicname + r.choice(possads)
        self.ethnicity = self.ethnicity.capitalize()
    def cityName(self):
        templates = ["cvccvc", "cvvcv", "cvvccv", "cvvcvv"]
        chosen = r.choice(templates)
        final = ""
        for letter in chosen:
            if letter == 'c':
                final += r.choice(self.consonants)
            elif letter == 'v':
                final += r.choice(self.vowels)
            else:
                final += letter
        final = final.capitalize()
        if r.randint(0,1) == 1:
            final += r.choice(self.suffixes)
        return final
    def personName(self):
        chosen = ""
        first = r.randint(0,1)
        for i in range(r.randint(3,4)):
            if(first == 1):
                chosen += r.choice(self.consonants)
            chosen += r.choice(self.vowels)
            if first == 0:
                chosen += r.choice(self.consonants)
        final = chosen + " "
        chosen = ""
        first = r.randint(0,1)
        for i in range(r.randint(3,6)):
            if(first == 1):
                chosen += r.choice(self.consonants)
            chosen += r.choice(self.vowels)
            if first == 0:
                chosen += r.choice(self.consonants)
        final += chosen
        return final

