import sys
from WordBuffer import WordBuffer
from automate import Automate
from ConstructAllTree import ConstructAllTree
from Projectivite import Projectivite
from Features import Features


class Oracle(Automate):

    """
    Objectif :
                    Construire les configurations et les transitions corespondantes d'un arbre
    """

    def __init__(self, target_tree, features):
        """
        constructor: Automate
        input:
                                        target_tree = Arbre objectif contenue dans un Tree
                                        features = liste des features à prendre en compte pour construire une configuration
        Initialise un automate avec les mots de la phrase
        labels est la liste des different labels de la phrase
        """
        sentence = list()
        for vt in target_tree.vertices:
            sentence.append(vt.get_word())

        Automate.__init__(self, sentence)
        self.target_tree = target_tree

        self.labels = list()
        for word in sentence:
            # print(word.getFeat('FORM'))
            l = word.getFeat('LABEL')
            if l is not None:  # Si l n'est pas liée au root
                if l not in self.labels:  # Si l n'est pas déjà dans la liste
                    self.labels.append(l)
        # print(self.labels)

        self.features = features

    def present_in_tree(self, tree, wi, l, wj):
        """
        Input :
                        tree : l'arbre dans lequel la recherche sera effectué
                        wi : l'indice du mot i
                        wj : l'indice du mot j
                        l : le label de la liaison (wi -> wj)
        Renvoie true si la liaison (wi, l, wj) est présente dans tree
        Sinon renvoie False
        """
        if wi == None or wj == None:
            return False

        vertex_i = tree.index_search(wi)
        # vertex_i.show_liaison()
        for liaison in vertex_i.nodes:
            if liaison.get_target().get_index() == wj:
                # print("aff",liaison.get_target().get_word().getFeat('FORM'))
                if liaison.get_label() == l:
                    return True
        return False

    def run(self):
        """
        Execute l'oracle sur phrase et ajoute à self.features.labels
        la suite de transitions qui génére self.target_tree ainsi que
        les configurations corespondantes à self.features.datas
        """

        while not self.fin():
            # self.tree.print_tree()
            flag = True

            Spile = self.pile.see(0)
            Sbuff = self.buff.see(0)
            # print("Spile : ", Spile, " Sbuff : ", Sbuff)

            self.features.extract_features(self.pile, self.buff, self.tree)

            # LEFT_l
            if Spile is not None:
                for l in self.labels:
                    if self.present_in_tree(self.target_tree, Sbuff, l, Spile):
                        # self.pile.push(Spile)
                        # self.buff.push(Sbuff)
                        self.left(l)
                        self.features.labels.append("LEFT_" + l)
                        #print("LEFT_" + l)
                        flag = False
                        break

            # RIGHT_l
            if flag and Spile is not None:
                for l in self.labels:
                    if self.present_in_tree(self.target_tree, Spile, l, Sbuff):
                        # self.pile.push(Spile)
                        # self.buff.push(Sbuff)
                        self.right(l)
                        self.features.labels.append("RIGHT_" + l)
                        #print("RIGHT_" + l)
                        flag = False
                        break

            # REDUCE
            if flag and Spile is not None:
                nb_dependant = 0
                nb_dependances = 0
                for vertex_i in self.tree.vertices:  # Pour tous les mots
                    # if vertex_i.parent == None:
                    #	continue
                    for l in self.labels:  # Pour tous les labels possible
                        # Si le Spile gouverne vertex
                        if self.present_in_tree(self.target_tree, Spile, l, vertex_i.get_index()):
                            nb_dependant += 1
                            #print(vertex_i.get_word()," Label ", l)
                            # if vertex_i.get_word() == 'Trois' and l == 'nummod':
                            #	sys.exit(0)
                            # Si cette liaison a déjà était ajouter a l'arbre
                            if self.present_in_tree(self.tree, Spile, l, vertex_i.get_index()):
                                nb_dependances += 1
                # print(nb_dependances,nb_dependant)
                # print(self.tree.vertices[Spile].get_word().getFeat('FORM'))
                # Si on a crée toutes les dépendances du sommet de pile
                if nb_dependances == nb_dependant or self.buff.len() == 0:
                    if self.tree.index_search(Spile).parent is not None or self.tree.vertices[Spile].get_word().getFeat('FORM') == "root":
                        # self.pile.push(Spile)
                        # self.buff.push(Sbuff)
                        self.reduce()
                        self.features.labels.append("REDUCE")
                        # print("REDUCE")
                        flag = False

            # SHIFT
            if flag:
                self.features.labels.append("SHIFT")
                # print("SHIFT")
                # self.pile.push(Spile)
                # self.buff.push(Sbuff)
                self.shift()

        return self.tree


"""
# Test de la classe Automate
# Appelle la méthodes run sur les phrases du fichier test.txt

# Lecture du fichier conllu
mcd =(('INDEX', 'INT'), ('FORM', 'INT'), ('LEMMA', 'INT'), ('POS', 'SYM'), ('X1', 'INT'), ('MORPHO', 'INT'), ('GOV', 'SYM'), ('LABEL', 'SYM'), ('X2', 'SYM'), ('X3', 'SYM'))
obj_generateAlltree = ConstructAllTree("test.txt",mcd,True)
all_tree = obj_generateAlltree.get_allTree()

for tree in all_tree:
	sentence = list()
	for vt in tree.vertices:
		sentence.append(vt.get_word())

	automate = Automate(sentence=sentence)
	tree = automate.run()
	tree.print_tree()
"""
if(__name__ == "__main__"):
# Test de la classe Oracle et Features
	mcd =(('INDEX', 'INT'), ('FORM', 'INT'), ('LEMMA', 'INT'), ('POS', 'SYM'), ('X1', 'INT'), ('MORPHO', 'INT'), ('GOV', 'SYM'), ('LABEL', 'SYM'), ('X2', 'SYM'), ('X3', 'SYM'))

	# Lecture du fichier conllu
	obj_generateAlltree = ConstructAllTree("test_conllu.txt", mcd, False)
	all_tree = obj_generateAlltree.get_allTree()

	features = Features("Data/f2_tbp.fm")

	for tree in all_tree:
		# tree.print_tree()

		A = Oracle(tree, features)

		result_tree = A.run()
		# result_tree.print_tree()

	print("Liste des données (X) :")
	#print(features.datas)
	print("Liste des labels (Y) :")
	#print(features.labels)
	print("Nb label : ", len(features.labels))
	print("Nb data : ", len(features.datas))
	
	onehot_X = features.convert_datas_to_one_hot()
	#print("Final X ", onehot_X)
	onehot_Y = labels_onehot = features.convert_labels_to_one_hot()
	#print("Final Y ", onehot_Y)
	
	print("Nombre de labels different : ",features.nombre_labels())
	
	print("Liste des mots réccuperer ",features.forms)
	print("Mots après embedding",features.convert_forms_to_embedding("Data/embd_file_vectors/embd.vec"))
	
"""
def printSentence(sentence, mcd):
	for i in range(0, len(sentence)):
		sentence[i].affiche(mcd)

wb = WordBuffer(mcd);
wb.readFromConlluFile("test.txt"); #../UD_Japanese-Modern/ja_modern-ud-test.conllu  ../UD_French-GSD/fr_gsd-ud-test.conllu

for i in range(0,int(sys.argv[1])):
	sentence = wb.nextSentence()

mots = list()
for j in range(0, len(sentence)):
	mots.append(sentence[j].getFeat('FORM'))
print("N° : ",i+1, mots)

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

while sentence:
	#print('sentence', sentNb)
	#printSentence(sentence, mcd)

	sentNb += 1
	sentence = wb.nextSentence()
"""
