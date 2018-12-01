from arbre import *
import random


class Automate:

    def __init__(self, pile, buff, tree):
        """
        constructor: Automate
        input:
                pile=Pile
                buff=Pile
                tree=Tree
                
                clf = Un classifieur entrainner
                features = Un objet features decrivant les features à utliser
        """
        self.pile = pile
        self.buff = buff
        self.tree = tree
        
        self.clf = clf
        self.features = features

    def __init__(self, sentence=[]):
        """
        constructor: Automate
        input:
                sentence = Word[]
        Initialise un automate avec les mots de la sentence (Constitué de Word)
        """
        self.pile = Pile()
        self.buff = Pile()
        for i in range(len(sentence)-1, -1, -1):
            self.buff.push(i)
        self.tree = Tree()
        self.tree.fill(sentence)

    def fin(self):
        """
        Return True si l'automate a terminer, False sinon
        """
        if self.pile.len() == 0 and self.buff.len() == 0:
            return True
        return False

    def shift(self):
        """
        Déplace le sommet du buffer au sommet de la pile
        """
        wi = self.buff.pop()
        self.pile.push(wi)

    def reduce(self):
        """
        Supprime le sommet de la pile si il a un père, sauf si c'est le 
        root (Car il n'as jamais de père)
        """
        wi = self.pile.pop()
        #print(wi)
        vertex = self.tree.index_search(wi)
        if vertex is not None:
            # Si il n'a pas de parent on annule l'action
            if vertex.parent is None and vertex.get_word().getFeat('FORM') is not "root":
                self.pile.push(wi)

    def right(self, label):
        """
        Crée une liaison du sommet de la pile vers le sommet du buffeur
        """
        wi = self.pile.pop()
        wj = self.buff.pop()
        #print(wi)

        self.tree.link(wi, label, wj)

        self.pile.push(wi)
        self.pile.push(wj)

    def left(self, label):
        """
        Crée une liaison du sommet du buffeur vers le sommet de la pile
        Seulement si le sommet de la pile n'as pas de parent
        """
        wi = self.pile.pop()
        #print(wi)
        vertex = self.tree.index_search(wi)
        if vertex is not None:
            # Si wi n'a pas de parent
            if vertex.parent is None:
                wj = self.buff.pop()

                self.tree.link(wj, label, wi)

                self.buff.push(wj)
            else:  # Si wi a déjà un parent on annule
                self.pile.push(wi)

    def run(self):
        """
        Execute l'automate sur la sentence et renvoie l'arbre obtenue
        """
        while not self.fin():
            #self.tree.print_tree()
            
            data, form = self.features.extract_features(self.pile, self.buff, self.tree)
            
            
            t =  clf.predit( # Oracle transition
            
            if t == 0:
                #print("shift")
                self.shift()
            elif t == 1:
                #print("reduce")
                self.reduce()
            elif t == 2:
                #print("right")
                l = random.choice(range(4))  # Oracle label
                self.right(l)
            elif t == 3:
                #print("left")
                l = random.choice(range(4))  # Oracle label
                self.left(l)

        return self.tree

"""
sentence = ["sami", "va", "à", "la", "école"]

automate = Automate(sentence=sentence)

# automate.tree.print_tree()

tree = automate.run()

tree.print_tree()
"""
