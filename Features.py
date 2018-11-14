import sys

class Features:
	"""
	Objectif : 
		Construire la liste des features présent dans un fichiers fm
		Et constitué le dataset corespndant au features
	"""
	
	def __init__(self, features_file):
		"""
		constructor: Features
		input:
				features_file = fichier contenant la liste des features
		Remplie la liste des features en lisant le fichier features_file
		"""
		self.names = list()
		
		# Lecture du fichier
		with open(features_file,'r') as f:
			lines = f.readlines()
		# Remplissage des noms 
		for line in lines:
			#print(line)
			line = line.split(".")
			line[-1] = line[-1].rstrip('\n')
			#print(line)
			
			if line[0] == 'S':
				idx = int(line[1])
				feat = line[2]
				self.names.append(("Pile",idx,feat))
			elif line[0] == 'B':
				idx = int(line[1])
				feat = line[2]
				self.names.append(("Buffer",idx,feat))
			else:
				self.names.append(line[0])
		print("Features prise en compte : ",self.names)
		
		# Dataset
		self.datas = list()
		self.labels = list()
		
	def extract_features(self, pile, buff, tree):
		"""
		input:
				pile = La pile courante
				buff = Le buffer courant
				tree = L'arbre courant
		Extrait les features de l'état courant (pile,buff,tree) et les 
		ajoute à self.datas
		"""
		data = list()
		
		for feature in self.names:
			print(feature)
			if feature[0] == 'Pile':
				idx = feature[1]
				feat = feature[2]
				idx_pile = pile.see(idx)
				if idx_pile != None:
					data.append(tree.vertices[idx_pile].get_elementWord(element=feat))
					#print(data)
				else:
					data.append('NA') # Donnée non aquise
										
			elif feature[0] == 'Buffer':
				idx_buff = feature[1]
				feat = feature[2]
				
				idx = buff.see(0)
				if idx == None: # Si le buffer est vide on ce place juste après le dernier mot
					idx = len(tree.vertices)
					
				if idx+idx_buff < 0 or idx+idx_buff >= len(tree.vertices): # Si la features concerne un élément hors de la phrase
					data.append('NA') # Donnée non aquise
				else:
					data.append(tree.vertices[idx+idx_buff].get_elementWord(element=feat))
					
			elif feature == 'DIST':
				Spile = pile.see(0)
				Sbuff = buff.see(0)
				if Spile != None and Sbuff != None:
					data.append(abs(tree.vertices[Spile].get_index() - tree.vertices[Sbuff].get_index()))
				else:
					data.append('NA') # Donnée non aquise
			
		self.datas.append(data)
		
		#print(data)
		return data

# Pour faire des One-hot
# https://machinelearningmastery.com/how-to-one-hot-encode-sequence-data-in-python/

if(__name__ == "__main__"):
	features = Features("f3_tbp.fm")
