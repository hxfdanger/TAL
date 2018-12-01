from Word import Word
import numpy as np


class Tree:

    def __init__(self):
        """
        constructor: Tree
        input: sentence list[string]
        """
        self.vertices=[]

    def fill(self, sentence=[]):
        """
        constructor: Tree
        input: sentence list[string]
        Création d'un arbre contenant un vertex par mots de la sentence
        Aucune liaison n'est crée
        """

        """
        self.vertices = []
        # Ajout de la racine
        vertex = Vertex("Root", 0, None, list())
        self.push(vertex)"""

        i=0  # Index dans la phrase
        for word in sentence:
            # Ajout des mots de la phrase dans l'arbre
            vertex=Vertex (word, None, list ())
            self.push (vertex)
            i+=1

    def push(self, vertex):
        """
        push vertex to the end of the tree
        """
        return self.vertices.append (vertex)

    def get_vertices(self):
        return self.vertices

    def pop(self):
        """
        return the first vertex in the tree
        """
        return self.vertices.pop (0)

    def print_tree(self):
        """
        Affiche l'arbre
        """
        for vertex in self.vertices:
            vertex.show_vertex ()
        print ()

    def index_search(self, index):
        """
        Retourne le iéme vertex de l'arbre
        """
        if index is not None:
            return self.vertices[index]
        return None

    def link(self, wi, label, wj):
        """
        input:
                wi=Indice dans le tableau vertices (gouverneur)
                label=string
                wj=Indice dans le tableau vertices (dependant)
        Crée une liaison de wi vers wj avec label
        """
        vertex_i=self.index_search (wi)
        vertex_j=self.index_search (wj)

        if vertex_i is not None and vertex_j is not None:
            liaison=Liaison (target=vertex_j, label=label)
            # print("add link here : vertex_i : ")
            # vertex_i.show_vertex()
            # print(" vertex_j : ")
            # vertex_j.show_vertex()
            vertex_i.add_link (liaison)
            vertex_j.set_parent (vertex_i)

    def create_link_vertex(self, vi, label, vj):
        """
        input:
                vi=Vertex
                label=string
                vj=Vertex
        Crée une liaison de vi vers vj avec label
        """
        if vi is not None and vj is not None:
            liaison=Liaison (target=vj, label=label)
            # print(" vertex .. add link here : vertex_i : ")
            # vi.show_vertex()
            # print(" vertex_j : ")
            # vj.show_vertex()
            vi.add_link (liaison)
            vj.set_parent (vi)

    def compare_tree(tree1, tree2):
        """
        ATENTION fonction qui ne marche pas !!

        Renvoie True si les deux arbre sont identique
        """
        if len (tree1.vertices) != len (tree2.vertices):
            return False

        for vertex1, vertex2 in zip (tree1.vertices, tree1.vertices):
            if vertex1.compare_vertex (vertex2) == False:
                return False
        return True

    def return_sous_arbre(self, index):
        """
        Renvoie le tableau (des indices) du sous arbres partant du noeud index
        index est l'indice du noeud racine du sous arbre
        """
        if index >= len (self.vertices) or index < 0:
            print ("Arbre : Impossible de calculer le sous arbre, l'index est hors du tableau")

        vertex=self.index_search (index)

        sous_arbre=list ()
        sous_arbre.append (vertex)

        for vertex in sous_arbre:
            # vertex.show_liaison()
            nodes=vertex.get_nodes ()

            targets=list ()
            for node in nodes:
                targets.append (node.get_target ())

            for target in targets:
                sous_arbre.append (target)

            """for i,vertex in enumerate(sous_arbre):
                print(vertex.get_index(),end=' ')
            print()"""

        for i, vertex in enumerate (sous_arbre):
            sous_arbre[i]=vertex.get_index ()

        return np.asarray (sous_arbre)


class Vertex:

    def __init__(self, word, parent, nodes=[]):
        """
        constructor: Vertex
        input:
                word=Word
                parent=Vertex
                nodes= Liaisons list[]
        """

        self.word=word
        self.parent=parent
        self.nodes=nodes

    def get_word(self):
        return self.word

    def get_index(self):
        return int (self.word.getFeat ("INDEX"))

    def get_labelWord(self):
        return self.word.getFeat ("FORM")

    def get_elementWord(self, element="LABEL"):
        return self.word.getFeat (element)

    def get_nodes(self):
        return self.nodes

    def get_link_dep_by_label(self, label):
        for vt in self.nodes:
            if (vt.label == label):
                return vt

    def get_link_dep(self, vertex):
        for vt in self.nodes:
            if (vt.target == vertex):
                return vt

    def delete_link_dep(self, vertex):
        for idx, vt in enumerate (self.nodes):
            if (vt.target == vertex):
                del self.nodes[idx]

    def get_all_deproj_link(self):
        listes_dep=list ()
        for idx, vt in enumerate (self.nodes):
            if (vt.label.find ("|") != -1):
                listes_dep.append (vt)
        return listes_dep

    def show_liaison(self):
        for node in self.nodes:
            print ("\t\tTarget (", node.get_target ().get_index (), ")", node.get_target ().get_labelWord ())
            print ("\t\tLabel :", node.get_label ())

    def show_parent(self):
        if self.parent is not None:
            print ("\tParent (", self.parent.get_index (), ") ",
                   self.parent.get_labelWord ())
        else:
            print ("\tParent : NO PARENT  ")

    def show_vertex(self):
        print (self.get_index (), "-Word \"%s\" " % self.get_labelWord ())
        self.show_parent ()
        if (len (self.nodes) > 0):
            print ("\tLiaisons")
        self.show_liaison ()

    def set_parent(self, parent):

        self.parent=parent

    def get_parent(self):
        return self.parent

    def add_link(self, liaison):
        """
        Input:
            liaison = Liaison
        Ajoute une liaison a la liste nodes
        """
        self.nodes.append (liaison)

    def compare_vertex(vertex1, vertex2):
        """
        ATENTION Non foncitonnel !!
        """
        if vertex1 == None or vertex2 == None:
            if vertex1 == None and vertex2 == None:
                return True
            else:
                return False

        if vertex1.get_index () != vertex2.get_index ():
            return False
        if vertex1.get_labelWord () != vertex2.get_labelWord ():
            return False
        if vertex1.get_elementWord () != vertex2.get_elementWord ():
            return False

        if vertex1.parent != None and vertex2.parent == None:
            return False
        if vertex1.parent == None and vertex2.parent != None:
            return False
        if vertex1.parent != None and vertex2.parent != None:
            if vertex1.parent.get_labelWord () != vertex2.parent.get_labelWord ():
                return False

        if len (vertex1.nodes) != len (vertex2.nodes):
            return False

        for node1, node2 in zip (vertex1.nodes, vertex2.nodes):
            if node1.label != node2.label:
                return False

        return True


class Liaison:

    def __init__(self, target=None, label=''):
        """
        input :
                target= Vertex
                label= String
        """

        self.target=target
        self.label=label

    def get_target(self):
        return self.target

    def get_label(self):
        return self.label


class Pile:
    def __init__(self):
        """
        """
        self.pile=[]

    def see(self, index):
        """
        Retourne, sans retrait, l'élément de la pile en position index
        en partant du sommet de la pile
        """
        if len (self.pile) > index and index >= 0:
            return self.pile[len (self.pile) - 1 - index]
        return None

    def push(self, index):
        """
        Place index au sommet de la pile
        """
        if index is not None:
            return self.pile.append (index)

    def pop(self):
        """
        Retire le sommet de la pile si elle n'est pas vide et le retourne
        """
        if len (self.pile) > 0:
            return self.pile.pop (len (self.pile) - 1)
        return None

    def len(self):
        return len (self.pile)

    def print_pile(self):
        for i in range (len (self.pile)):
            print (self.pile[i], end=' ')
        print ()