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
        """
        self.pile = pile
        self.buff = buff
        self.tree = tree

    def __init__(self, sentence=[]):
        """
        constructor: Automate
        input:
                sentence = String[]
        Initialise un automate avec les mots de la sentence
        """
        self.pile = Pile()
        self.pile.push("Root")
        self.buff = Pile()
        for word in reversed(sentence):
            self.buff.push(word)
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
        Supprime le sommet de la pile si il a un père
        """
        wi = self.pile.pop()
        print(wi)
        vertex = self.tree.search(wi)
        if vertex is not None:
            # Si il n'a pas de parent on annule l'action
            if vertex.parent is None:
                self.pile.push(wi)

    def right(self, label):
        """
        Crée une liaison du sommet de la pile vers le sommet du buffeur
        """
        wi = self.pile.pop()
        wj = self.buff.pop()
        print(wi)

        l = list()
        l.append(label)
        self.tree.link(wi, l, wj)

        self.pile.push(wi)
        self.pile.push(wj)

    def left(self, label):
        """
        Crée une liaison du sommet du buffeur vers le sommet de la pile
        Seulement si le sommet de la pile n'as pas de parent
        """
        wi = self.pile.pop()
        print(wi)
        vertex = self.tree.search(wi)
        if vertex is not None:
            # Si wi n'a pas de parent
            if vertex.parent is None:
                wj = self.buff.pop()

                l = list()
                l.append(label)
                self.tree.link(wi, l, wj)

                self.buff.push(wj)
            else:  # Si wi a déjà un parent on annule
                self.pile.push(wi)

    def run(self):
        """
        Execute l'automate sur la sentence et renvoie l'arbre obtenue
        """
        while not self.fin():
            self.tree.print_tree()
            t = random.choice(range(4))  # Oracle transition
            if t == 0:
                print("shift")
                self.shift()
            elif t == 1:
                print("reduce")
                self.reduce()
            elif t == 2:
                print("right")
                l = random.choice(range(4))  # Oracle label
                self.right(l)
            elif t == 3:
                print("left")
                l = random.choice(range(4))  # Oracle label
                self.left(l)

        return self.tree


sentence = ["sami", "va", "à", "la", "école"]

automate = Automate(sentence=sentence)

# automate.tree.print_tree()

tree = automate.run()

tree.print_tree()
