import sys
from WordBuffer import WordBuffer
from automate import Automate

class Oracle(Automate):
	def __init__(self, datas, sentence=[]):
		"""
		constructor: Automate
		input:
				sentence = String[]
				datas = Informations des mots de la phrase dans un WordBuffer
		Initialise un automate avec les mots de la sentence et les datas
		"""
		Automate.__init__(self,sentence)
		self.datas = datas
		
		self.labels = list()
		for word in datas:
			l = word.getFeat('LABEL')
			if l not in self.labels:
				self.labels.append(l)
	
	def present_dans_datas(self, word_i, l, word_j):
		"""
		Renvoie true si la liaison (word_i, l, word_j) est présente dans
		self.datas
		Sinon renvoie False
		"""
		if word_i == None or word_j == None:
			return False
		
		for i in range(1, len(self.datas)): # Pour chaques mots de la phrase
			if(self.datas[i].getFeat('FORM') == word_j): # Si le mots est wj
				index_wi = int(self.datas[i].getFeat('GOV'))
				if(self.datas[index_wi].getFeat('FORM') == word_i): # Si le gouvernant de wj est wi
					if(self.datas[i].getFeat('LABEL') == l): # Si leurs label est l
						return True
		return False
		
	def present_dans_tree(self, word_i, l, word_j):
		"""
		Renvoie true si la liaison (wordi, l, wordj) est présente dans
		self.tree
		Sinon renvoie False
		"""
		if word_i == None or word_j == None:
			return False
		
		vertex_i = self.tree.search(word_i)
		vertex_i.show_liaison()
		for liaison in vertex_i.nodes:
			if liaison.get_target().get_word() == word_j:
				print("aff",liaison.get_target().get_word())
				if liaison.get_label() == l:
					return True
		return False
	
	def run(self):
		"""
		Execute l'oracle sur la sentence et renvoie la suite de 
		transitions qui génére l'arbre contenue dans WordBufferSentence
		"""
		while not self.fin():
			#self.tree.print_tree()
			flag = True
			
			Spile = self.pile.pop()
			Sbuff = self.buff.pop()
			print("Spile : ",Spile," Sbuff : ",Sbuff)
			
			# LEFT_l
			if Spile is not None:
				for l in self.labels:
					if self.present_dans_datas(Sbuff,l,Spile):
						self.pile.push(Spile)
						self.buff.push(Sbuff)
						self.left(l)
						print("LEFT_",l)
						flag = False
						break
			
			# RIGHT_l			
			if flag and Spile is not None:
				for l in self.labels:
					if self.present_dans_datas(Spile,l,Sbuff):
						self.pile.push(Spile)
						self.buff.push(Sbuff)
						self.right(l)
						print("RIGHT_",l)
						flag = False
						break
			
			# REDUCE			
			if flag and Spile is not None:
				nb_dependant = 0
				nb_dependances = 0
				for vertex_i in self.tree.vertices: # Pour tous les mots
					#if vertex_i.parent == None:
					#	continue
					for l in self.labels: # Pour tous les labels possible
						if self.present_dans_datas(Spile,l,vertex_i.get_word()): # Si le Spile gouverne vertex
							nb_dependant+=1
							print(vertex_i.get_word()," Label ", l)
							#if vertex_i.get_word() == 'Trois' and l == 'nummod':
							#	sys.exit(0)
							if self.present_dans_tree(Spile,l,vertex_i.get_word()): # Si cette liaison a déjà était ajouter a l'arbre
								nb_dependances+=1	
				print(nb_dependances,nb_dependant)
				if nb_dependances == nb_dependant and nb_dependant > 0 or self.buff.len() == 0: # Si on a crée toutes les dépendances du sommet de pile
					if self.tree.search(Spile).parent is not None:
						self.pile.push(Spile)
						self.buff.push(Sbuff) 
						self.reduce()
						print("REDUCE")
						flag = False	
			
			# SHIFT			
			if flag:
				print("SHIFT")
				self.pile.push(Spile)
				self.buff.push(Sbuff)
				self.shift()

		return self.tree



mcd =(('INDEX', 'INT'), ('FORM', 'INT'), ('LEMMA', 'INT'), ('POS', 'SYM'), ('X1', 'INT'), ('MORPHO', 'INT'), ('GOV', 'SYM'), ('LABEL', 'SYM'), ('X2', 'SYM'), ('X3', 'SYM'))

#wb.affiche(mcd)

def printSentence(sentence, mcd):
	for i in range(0, len(sentence)):
		sentence[i].affiche(mcd)

wb = WordBuffer(mcd);
wb.readFromConlluFile("../UD_French-GSD/fr_gsd-ud-test.conllu");

for i in range(17):
	sentence = wb.nextSentence()
	sentNb = 1
#print(sentence[2].getFeat('FORM'))

mots = list()
for i in range(0, len(sentence)):
	mots.append(sentence[i].getFeat('FORM'))
print(mots)

A = Oracle(sentence,mots)
tree = A.run()
tree.print_tree()


"""
while sentence:
	#print('sentence', sentNb)
	#printSentence(sentence, mcd)
		
	sentNb += 1
	sentence = wb.nextSentence()
"""
