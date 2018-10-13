from arbre import * 

class Automate:
	
    def __init__(self,pile,buff,tree):
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

    def shift():
        """
		Déplace le sommet du buffer au sommet de la pile
        """
        wi = self.buff.pop()
        self.pile.push(wi)

    def reduce():
        """
		Supprime le sommet de la pile si il a un père
        """
        wi = self.pile.pop()
        vertex = self.tree.search(wi)
        if vertex is not None:
			# Si il n'a pas de parent on annule l'action
			if vertex.parent is None: 
				self.pile.push(wi)
    
    def right(label):
        """
		Crée une liaison du sommet de la pile vers le sommet du buffeur
        """
        wi = self.pile.pop()
        wj = self.buff.pop()
        
        l = list()
        l.append(label)
        self.tree.link(wi,l,wj)	
        
        self.pile.push(wi)
        self.pile.push(wj)		

    def left(label):
        """
		Crée une liaison du sommet du buffeur vers le sommet de la pile
		Seulement si le sommet de la pile n'as pas de parent
        """
        wi = self.pile.pop()
        vertex = self.tree.search(wi)
        if vertex is not None:
			# Si wi n'a pas de parent
			if vertex.parent is None:
				wj = self.buff.pop()
				
				l = list()
				l.append(label)
				self.tree.link(wi,l,wj)
				
				self.buff.push(wj)	
