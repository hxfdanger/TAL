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
		Labels est la liste des different labels de la phrase
		"""
		Automate.__init__(self,sentence)
		self.datas = datas
		
		self.labels = list()
		for word in datas:
			l = word.getFeat('LABEL')
			if l not in self.labels:
				self.labels.append(l)
	
	def present_dans_datas(self, wi, l, wj):
		"""
		Input :
			wi : l'indice du mot i
			wj : l'indice du mot j
			l : le label de la liaison (wi -> wj) 
		Renvoie true si la liaison (wi, l, wj) est présente dans
		self.datas
		Sinon renvoie False
		"""
		if wi == None or wj == None:
			return False
		
		for j in range(1, len(self.datas)): # Pour chaques mots de la phrase
			if(int(self.datas[j].getFeat('INDEX')) == wj): # Si le mots est wj
				if(int(self.datas[j].getFeat('GOV')) == wi): # Si le gouvernant de wj est wi
					if(self.datas[j].getFeat('LABEL') == l): # Si leurs label est l
						return True
		return False
		
	def present_dans_tree(self, wi, l, wj):
		"""
		Input :
			wi : l'indice du mot i
			wj : l'indice du mot j
			l : le label de la liaison (wi -> wj) 
		Renvoie true si la liaison (wi, l, wj) est présente dans
		self.tree
		Sinon renvoie False
		"""
		if wi == None or wj == None:
			return False
		
		vertex_i = self.tree.index_search(wi)
		#vertex_i.show_liaison()
		for liaison in vertex_i.nodes:
			if liaison.get_target().get_index() == wj:
				#print("aff",liaison.get_target().get_word())
				if liaison.get_label() == l:
					return True
		return False
	
	def run(self):
		"""
		Execute l'oracle sur la sentence et renvoie la suite de 
		transitions qui génére l'arbre contenue dans datas
		"""
		transitions = list()
		
		while not self.fin():
			#self.tree.print_tree()
			flag = True
			
			Spile = self.pile.pop()
			Sbuff = self.buff.pop()
			#print("Spile : ",Spile," Sbuff : ",Sbuff)
			
			# LEFT_l
			if Spile is not None:
				for l in self.labels:
					if self.present_dans_datas(Sbuff,l,Spile):
						self.pile.push(Spile)
						self.buff.push(Sbuff)
						self.left(l)
						transitions.append("LEFT_"+l)
						flag = False
						break
			
			# RIGHT_l			
			if flag and Spile is not None:
				for l in self.labels:
					if self.present_dans_datas(Spile,l,Sbuff):
						self.pile.push(Spile)
						self.buff.push(Sbuff)
						self.right(l)
						transitions.append("RIGHT_" + l)
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
						if self.present_dans_datas(Spile,l,vertex_i.get_index()): # Si le Spile gouverne vertex
							nb_dependant+=1
							#print(vertex_i.get_word()," Label ", l)
							#if vertex_i.get_word() == 'Trois' and l == 'nummod':
							#	sys.exit(0)
							if self.present_dans_tree(Spile,l,vertex_i.get_index()): # Si cette liaison a déjà était ajouter a l'arbre
								nb_dependances+=1	
				#print(nb_dependances,nb_dependant)
				if nb_dependances == nb_dependant or self.buff.len() == 0: # Si on a crée toutes les dépendances du sommet de pile
					if self.tree.index_search(Spile).parent is not None or self.tree.vertices[Spile].get_word() == "ROOT":
						self.pile.push(Spile)
						self.buff.push(Sbuff) 
						self.reduce()
						transitions.append("REDUCE")
						flag = False	
			
			# SHIFT			
			if flag:
				transitions.append("SHIFT")
				self.pile.push(Spile)
				self.buff.push(Sbuff)
				self.shift()
		
		print("")
		return self.tree, transitions



mcd =(('INDEX', 'INT'), ('FORM', 'INT'), ('LEMMA', 'INT'), ('POS', 'SYM'), ('X1', 'INT'), ('MORPHO', 'INT'), ('GOV', 'SYM'), ('LABEL', 'SYM'), ('X2', 'SYM'), ('X3', 'SYM'))

#wb.affiche(mcd)

def printSentence(sentence, mcd):
	for i in range(0, len(sentence)):
		sentence[i].affiche(mcd)

wb = WordBuffer(mcd);
wb.readFromConlluFile("../UD_French-GSD/fr_gsd-ud-test.conllu"); #../UD_Japanese-Modern/ja_modern-ud-test.conllu

for i in range(0,int(sys.argv[1])):
	sentence = wb.nextSentence()
	
mots = list()
for j in range(0, len(sentence)):
	mots.append(sentence[j].getFeat('FORM'))
print("N° : ",i+1, mots)

A = Oracle(sentence,mots)
tree, transitions = A.run()
tree.print_tree()
print(transitions)

"""
for i in range(0,104):
	sentence = wb.nextSentence()

for i in range(1,int(sys.argv[1])):
	sentence = wb.nextSentence()
	
	mots = list()
	for j in range(0, len(sentence)):
		mots.append(sentence[j].getFeat('FORM'))
	print("N° : ",i, mots)
	
	A = Oracle(sentence,mots)
	tree = A.run()
"""





"""
while sentence:
	#print('sentence', sentNb)
	#printSentence(sentence, mcd)
		
	sentNb += 1
	sentence = wb.nextSentence()
"""
