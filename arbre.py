class Tree:

	def __init__(self):
		"""
		constructor: Tree
		input: sentence list[string]
		"""
		self.vertices = []
		
	def __init__(self,sentence=[]):
		"""
		constructor: Tree
		input: sentence list[string]
		Création d'un arbre contenant un vertex par mots de la sentence
		Aucune liaison n'est crée
		"""
		self.vertices = []
		# Ajout de la racine
		vertex = Vertex("Root",0,None,list())
		self.vertices.append(vertex)
		
		i = 1 # Index dans la phrase
		for word in sentence:
			# Ajout des mots de la phrase dans l'arbre
			vertex = Vertex(word,i,None,list())
			self.vertices.append(vertex)
			i+=1
		
	def push(vertex):
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
			print("Indice ",vertex.index," Word ",vertex.word)
			if vertex.parent is not None:
				print("\tParent (",vertex.parent.index,") ",vertex.parent.word)
			for liaison in vertex.nodes:
				print("\tTarget ",liaison.target)
		
	def search(word):
		"""
		Retourne le vertex qui contient word si il existe
		Sinon retourne None
		"""
		for vertex in self.vertices:
			if vertex.word == word:
				return vertex
		return None

	def link(word_i,labels,word_j):
		"""
		input:
			wordi_i=string
			labels=string[]
			word_j=string
		Crée une liaison de wi vers wj avec labels
		"""
		vertex_i = self.tree.search(word_i)
		vertex_j = self.tree.search(word_j)
		if vertex_i is not None and vertex_j is not None:
			liaison = Liaison(index=vertex_j, labels=labels)
			vertex_i.nodes.append(liaison)
			vertex_j.parent = vertex_i
 
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


class Liaison:

	def __init__(self, target, labels=[]):
		"""
		input :
			target= Vertex
			labels= String[]
		"""

		self.target = target
		self.labels = labels


class Pile:

	def __init__(self):
		"""
		"""
		self.pile = []

	def push(self,word):
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
