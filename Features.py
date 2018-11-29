import sys
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import OneHotEncoder

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
			line = line.split(".")
			line[-1] = line[-1].rstrip('\n')
			
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
		
		# OneHot encoders pour crée les vecteurs one hot
		self.oneHot_encoders = list()
		for features in self.names:
			self.oneHot_encoders.append(OneHotEncoder(sparse=False,handle_unknown='ignore'))
		
	def extract_features(self, pile, buff, tree):
		"""
		input:
				pile = La pile courante
				buff = Le buffer courant
				tree = L'arbre courant
		Extrait les features de l'état courant (pile,buff,tree) et les 
		ajoute à self.datas
		"""
		data = list() # Liste des features de l'états courant
		
		for feature in self.names: # Pour toutes les features connues
			print(feature)
			if feature[0] == 'Pile': # Si la feature concerne la pile
				idx = feature[1]
				feat = feature[2]
				idx_pile = pile.see(idx)
				if idx_pile != None:
					data.append(tree.vertices[idx_pile].get_elementWord(element=feat))
					#print(data)
				else:
					data.append('NA') # Donnée non aquise
										
			elif feature[0] == 'Buffer': # Si la feature concerne le buffer
				idx_buff = feature[1]
				feat = feature[2]
				
				idx = buff.see(0)
				if idx == None: # Si le buffer est vide on ce place juste après le dernier mot
					idx = len(tree.vertices)
					
				if idx+idx_buff < 0 or idx+idx_buff >= len(tree.vertices): # Si la features concerne un élément hors de la phrase
					data.append('NA') # Donnée non aquise
				else:
					data.append(tree.vertices[idx+idx_buff].get_elementWord(element=feat))
					
			elif feature == 'DIST': # Si la feature est une distance
				Spile = pile.see(0)
				Sbuff = buff.see(0)
				if Spile != None and Sbuff != None:
					data.append(abs(tree.vertices[Spile].get_index() - tree.vertices[Sbuff].get_index()))
				else:
					data.append('NA') # Donnée non aquise
			
		self.datas.append(data)
		
		#print(data)
		return data
		
	def convert_data_to_one_hot(self,data):
		"""
		Converti la liste de features data en un tableau 1D de vecteur one hot 
		"""
		if len(data) != len(self.names):
			print("La donnée ne posséde pas autant de features que demander !")
			return None
		
		new_data = list()
		for i,feature in enumerate(data):
			tmp = np.array(feature).reshape(1, -1)
			tmp = self.oneHot_encoders[i].transform(tmp)
			new_data.append(tmp.reshape(-1))
			
		new_data = np.asarray(new_data)
		new_data = new_data.flatten()
		print(new_data)	
		return new_data
		
	def convert_datas_to_one_hot(self):
		"""
		Entrainent les labels encoders sur le dataset
		Converti les self.datas en une liste de liste de vecteur one hot
		"""
		if len(self.datas) <= 0:
			print("Le dataset est vide, il est impossible d'entrainer les labels encoders!")
			return None
			
		# Entrainment des oneHot_encoders
		values = np.array(self.datas)
		#values = values.reshape(np.shape(values)[0],np.shape(values)[1], 1)
		for i,encoder in enumerate(self.oneHot_encoders):
			print("Values = ",values[:,i])
			encoder = encoder.fit(values[:,i].reshape(-1, 1))
		
		# Convertion du dataset
		for data in self.datas:
			data = self.convert_data_to_one_hot(data)
		
		return self.datas
		
# Pour faire des One-hot
# https://machinelearningmastery.com/how-to-one-hot-encode-sequence-data-in-python/

if(__name__ == "__main__"):
	features = Features("Data/f3_tbp.fm")
