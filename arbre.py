class Tree:

    def __init__(self):
        """
        constructor: Tree
        input: sentence list[string]
        """
        self.vertices = []

    def fill(self, sentence=[]):
        """
        constructor: Tree
        input: sentence list[string]
        Création d'un arbre contenant un vertex par mots de la sentence
        Aucune liaison n'est crée
        """
        self.vertices = []
        # Ajout de la racine
        vertex = Vertex("Root", 0, None, list())
        self.push(vertex)

        i = 1  # Index dans la phrase
        for word in sentence:
            # Ajout des mots de la phrase dans l'arbre
            vertex = Vertex(word, i, None, list())
            self.push(vertex)
            i += 1

    def push(self, vertex):
        """
        push vertex to the end of the tree
        """
        return self.vertices.append(vertex)

    def pop():
        """
        return the first vertex in the tree
        """
        return self.vertices.pop(0)

    def print_tree(self):
        """
        Affiche l'arbre
        """
        for vertex in self.vertices:
            vertex.show_vertex()

    def search(self, word):
        """
        Retourne le vertex qui contient word si il existe
        Sinon retourne None
        """
        for vertex in self.vertices:
            if vertex.get_word() == word:
                return vertex
        return None

    def link(self, word_i, labels, word_j):
        """
        input:
                wordi_i=string
                labels=string[]
                word_j=string
        Crée une liaison devertex.show_liaison() wi vers wj avec labels
        """
        vertex_i = self.search(word_i)
        vertex_j = self.search(word_j)
        if vertex_i is not None and vertex_j is not None:
            liaison = Liaison(index=vertex_j, labels=labels)
            vertex_i.add_link(liaison)
            vertex_j.set_parent(vertex_i)


class Vertex:

    def __init__(self, word, index, parent, nodes=[]):
        """
        constructor: Vertex
        input:
                word=string
                index=int
                parent=Vertex
                nodes= Liaisons list[]
        """

        self.word = word
        self.index = index
        self.parent = parent
        self.nodes = nodes

    def get_word(self):
        return self.word

    def get_index(self):
        return self.index

    def show_liaison(self):
        for node in self.nodes:
            print("\tTarget ", node.get_target())
            print("\tType Laison : ", node.get_labels())

    def show_parent(self):
        if self.parent is not None:
            print("\tParent (", self.parent.get_index(), ") ",
                  vertex.parent.get_word())

    def show_vertex(self):
        print("Indice ", self.get_index(), " Word ", self.get_word())
        self.show_parent()
        self.show_liaison()

    def set_parent(self, parent):
        self.parent = parent

    def add_link(self, liaison):
        """
        il manque le label à ajouter
        """
        self.nodes.append(liaison)


class Liaison:

    def __init__(self, target, labels=[]):
        """
        input :
                target= Vertex
                labels= String[]
        """

        self.target = target
        self.labels = labels

        def get_target(self):
            return self.target

        def get_labels(self):
            return self.labels


class Pile:
    def __init__(self):
        """
        """
        self.pile = []

    def push(self, word):
        """

        """
        return self.pile.append(word)

    def pop(self):
        """

        """
        if len(self.pile) > 0:
            return self.pile.pop(len(self.pile) - 1)
        return None

    def len(self):
        return len(self.pile)
