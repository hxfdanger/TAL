class Tree:

    def __init__(self):
        """
        constructor: Tree
        input: sentence list[string]
        """
        self.vertices = []

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
        Crée une liaison de wi vers wj avec label 
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

    def __init__(self, index, labels=[]):
        """

        """

        self.index = index
        self.labels = labels


class Pile:

    def __init__(self):
        """
        """
        self.pile = []

    def push(word):
        """

        """
        return self.pile.append(word)

    def pop():
        """

        """
        return self.pile.pop(len(self.pile) - 1)
