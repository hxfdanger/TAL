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

	######################  Ibrahim ########################################
	def index_search(self, idx):
		"""
		Retourne le vertex qui contient word si il existe
		Sinon retourne None
		"""
		for vertex in self.vertices:
			if vertex.get_index() == idx:
				return vertex
		return None

	def create_link_vertex(self, vi, label, vj):
		"""
		input:
				wordi_i=string
				label=string
				word_j=string
		Crée une liaison de wi vers wj avec label
		"""



		if vi is not None and vj is not None:
			liaison = Liaison(target=vj, label=label)
			print(" vertex .. add link here : vertex_i : ")
			vi.show_vertex()
			print(" vertex_j : ")
			vj.show_vertex()
			vi.add_link(liaison)
			vj.set_parent(vi)

	##############################################################

	def link(self, word_i, label, word_j):
		"""
		input:
				wordi_i=string
				label=string
				word_j=string
		Crée une liaison de wi vers wj avec label
		"""
		vertex_i = self.search(word_i)
		vertex_j = self.search(word_j)


		if vertex_i is not None and vertex_j is not None:
			liaison = Liaison(target=vertex_j, label=label)
			print("add link here : vertex_i : ")
			vertex_i.show_vertex()
			print(" vertex_j : ")
			vertex_j.show_vertex()
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

    ############Code ajouter par ibrahim #######################


	def get_nodes(self):
	    return self.nodes

	def get_link_dep_by_label(self, label):
		for vt in self.nodes:
			if (vt.label == label):
				return vt

	def get_link_dep(self,vertex):
		for vt in self.nodes:
			if (vt.target == vertex):
				return vt





	def delete_link_dep(self,vertex):
		for idx,vt in enumerate(self.nodes):
			if(vt.target == vertex):
				  del self.nodes[idx]


	def get_all_deproj_link(self):
			listes_dep = list()
			for idx, vt in enumerate(self.nodes):
				if (vt.label.find("|") != -1):
					listes_dep.append(vt)
			return listes_dep


	############################################################

	def show_liaison(self):
		for node in self.nodes:
			print("\tTarget ", node.get_target().get_word())
			print("\tType Laison : ", node.get_label())

	def show_parent(self):
		if self.parent is not None:
			print("\tParent (", self.parent.get_index(), ") ",
				  self.parent.get_word())
		else:
			print("\tParent : NO PARENT  ")

	def show_vertex(self):
		print("Indice ", self.get_index(), " Word \"%s\" " % self.get_word())
		self.show_parent()
		self.show_liaison()

	def set_parent(self, parent):
		self.parent = parent
		
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

	def push(self, word):
		"""

		"""
		if word is not None:
			return self.pile.append(word)

	def pop(self):
		"""

		"""
		if len(self.pile) > 0:
			return self.pile.pop(len(self.pile) - 1)
		return None

	def len(self):
		return len(self.pile)
