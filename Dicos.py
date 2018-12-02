class Dicos:
    def __init__(self, mcd=False, fileName=False, verbose=False):
        self.content = {}
        self.locked = False
        if mcd:
            for elt in mcd:
                name, status = elt
                if(status == 'SYM'):
                    self.content[name] = ['NULL', 'ROOT']
        elif fileName:
            try:
                dicoFile = open(fileName, encoding='utf-8')
            except IOError:
                print(fileName, 'does not exist')
                exit(1)
            for ligne in dicoFile:
                if ligne[0] == '#' and ligne[1] == '#':
                    currentDico = ligne[2:-1]
                    self.content[currentDico] = []
                    if(verbose):
                        print('in module', __name__,
                              'create dico', currentDico)
                else:
                    value = ligne[:-1]
                    if not value in self.content[currentDico]:
                        self.content[currentDico].append(value)
                        if(verbose):
                            print('in module', __name__, 'adding entry',
                                  value, 'to', currentDico)
            dicoFile.close()
            self.lock()

    def populateFromMcfFile(self, mcfFilename, mcd, verbose=False):
        try:
            mcfFile = open(mcfFilename, encoding='utf-8')
        except IOError:
            print('cannot open', mcfFilename)
            exit(1)
            tokens = []
        for ligne in mcfFile:
            tokens = ligne.split()
            for i in range(0, len(tokens)):
                if mcd[i][1] == 'SYM':
                    if not tokens[i] in self.content[mcd[i][0]]:
                        self.content[mcd[i][0]].append(tokens[i])
                        if(verbose):
                            print('in module:', __name__, 'adding value ',
                                  tokens[i], 'to dico', mcd[i][0])
        mcfFile.close()
        for e in self.content:
            print('DICO', e, ':\t', len(self.content[e]), 'entries')

    def populateFromConlluFile(self, conlluFilename, verbose=False):
        try:
            conlluFile = open(conlluFilename, encoding='utf-8')
        except IOError:
            print('cannot open', conlluFilename)
            exit(1)
        mcd = (('INDEX', 'INT'), ('FORM', 'INT'), ('LEMMA', 'INT'), ('POS', 'SYM'), ('X1', 'INT'),
               ('MORPHO', 'INT'), ('GOV', 'SYM'), ('LABEL', 'SYM'), ('X2', 'SYM'), ('X3', 'SYM'))
        tokens = []
        h = 0
        for ligne in conlluFile:
            #print("Ligne : ",h)
            h += 1
            if ligne[0] != '\n' and ligne[0] != '#':
                tokens = ligne.split("\t")
                for i in range(0, len(tokens)):
                    if mcd[i][1] == 'SYM':
                        if not tokens[i] in self.content[mcd[i][0]]:
                            self.content[mcd[i][0]].append(tokens[i])
                            if(verbose):
                                print('in module:', __name__, 'adding value ',
                                      tokens[i], 'to dico', mcd[i][0])
        conlluFile.close()
        for e in self.content:
            print('DICO', e, ':\t', len(self.content[e]), 'entries')

    def lock(self):
        self.locked = True
        for key in self.content.keys():
            self.content[key] = tuple(self.content[key])

    def print(self):
        for dico in self.content.keys():
            print(dico, self.content[dico])

    def printToFile(self, filename):
        try:
            dicoFile = open(filename, 'w', encoding='utf-8')
        except IOError:
            print('cannot open', filename)
            exit(1)
        for dico in self.content.keys():
            dicoFile.write('##')
            dicoFile.write(dico)
            dicoFile.write('\n')
            for elt in self.content[dico]:
                dicoFile.write(elt)
                dicoFile.write('\n')
        dicoFile.close()

    def getCode(self, dicoName, symbol, verbose=False):
        if(verbose):
            print('in module ', __name__, 'getCode(', dicoName, ',', symbol, ')')
        if not self.locked:
            print('Dicos must be locked before they can be accessed')
            return False
        if not dicoName in self.content:
            print('no such dico as', dicoName)
            return False
#                print('dicoName =', dicoName, 'symbol =', symbol)
        return self.content[dicoName].index(symbol)

    def getSymbol(self, dicoName, code):
        if not self.locked:
            print('Dicos must be locked before they can be accessed')
            return False
        if not dicoName in self.content:
            print('no such dico as', dicoName)
            return False
        return self.content[dicoName][code]

    def add(self, dicoName, symbol):
        if not dicoName in self.content:
            self.content[dicoName] = {symbol}
        else:
            self.content[dicoName].add(symbol)
