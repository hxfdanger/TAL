from Word import Word


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

        """
		self.vertices = []
		# Ajout de la racine
		vertex = Vertex("Root", 0, None, list())
		self.push(vertex)"""

        i = 0  # Index dans la phrase
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

    def get_vertices(self):
        return self.vertices

    def pop(self):
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

    def index_search(self, index):
        """
		Retourne le iéme vertex de l'arbre
		"""
        return self.vertices[index]

    def link(self, wi, label, wj):
        """
		input:
				wi=Indice dans le tableau vertices
				label=string
				wj=Indice dans le tableau vertices
		Crée une liaison de wi vers wj avec label
		"""
        vertex_i = self.index_search(wi)
        vertex_j = self.index_search(wj)

        if vertex_i is not None and vertex_j is not None:
            liaison = Liaison(target=vertex_j, label=label)
            # print("add link here : vertex_i : ")
            # vertex_i.show_vertex()
            # print(" vertex_j : ")
            # vertex_j.show_vertex()
            vertex_i.add_link(liaison)
            vertex_j.set_parent(vertex_i)

    def create_link_vertex(self, vi, label, vj):
        """
		input:
				vi=Vertex
				label=string
				vj=Vertex
		Crée une liaison de vi vers vj avec label
		"""
        if vi is not None and vj is not None:
            liaison = Liaison(target=vj, label=label)
            print(" vertex .. add link here : vertex_i : ")
            #vi.show_vertex()
            print(" vertex_j : ")
            #vj.show_vertex()
            vi.add_link(liaison)
            vj.set_parent(vi)


class Vertex:

    def __init__(self, word, parent, nodes=[]):
        """
		constructor: Vertex
		input:
				word=Word

				parent=Vertex
				nodes= Liaisons list[]
		"""

        self.word = word
        self.parent = parent
        self.nodes = nodes

    def get_word(self):
        return self.word

    def get_index(self):
        return int(self.word.getFeat("INDEX"))

    def get_labelWord(self):
        return self.word.getFeat("FORM")

    def get_elementWord(self,element = "LABEL"):
        return self.word.getFeat(element)



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
        for idx, vt in enumerate(self.nodes):
            if (vt.target == vertex):
                del self.nodes[idx]

    def get_all_deproj_link(self):
        listes_dep = list()
        for idx, vt in enumerate(self.nodes):
            if (vt.label.find("|") != -1):
                listes_dep.append(vt)
        return listes_dep

    def show_liaison(self):
        for node in self.nodes:
            print("\t\tTarget (", node.get_target().get_index(), ")", node.get_target().get_labelWord())
            print("\t\tLabel :", node.get_label())

    def show_parent(self):
        if self.parent is not None:
            print("\tParent (", self.parent.get_index(), ") ",
                  self.parent.get_labelWord())
        else:
            print("\tParent : NO PARENT  ")

    def show_vertex(self):
        print(self.get_index(), "-Word \"%s\" " % self.get_labelWord())
        self.show_parent()
        if (len(self.nodes) > 0):
            print("\tLiaisons")
        self.show_liaison()

    def set_parent(self, parent):

        self.parent = parent

    def get_parent(self):
        return self.parent

    def add_link(self, liaison):
        """
		Input:
			liaison = Liaison
		Ajoute une liaison a la liste nodes
		"""
        self.nodes.append(liaison)


class Liaison:

    def __init__(self, target=None, label=''):
        """
		input :
				target= Vertex
				label= String
		"""

        self.target = target
        self.label = label

    def get_target(self):
        return self.target

    def get_label(self):
        return self.label


class Pile:
    def __init__(self):
        """
		"""
        self.pile = []

    def push(self, index):
        """

		"""
        if index is not None:
            return self.pile.append(index)

    def pop(self):
        """

		"""
        if len(self.pile) > 0:
            return self.pile.pop(len(self.pile) - 1)
        return None

    def len(self):
        return len(self.pile)
