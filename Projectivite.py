
from automate import *

class Projectivite:
	"""
	Class qui prend en entre une structure d'arbre et renvoit
	par la methode projectivise l'arbre projectivise ou
	deprojectise par la methode deprojectivser

	"""

	__author__ = "ibrahim souleiman"




	def projectiviser(self,tree):
		"""

		:param tree: Object tree
		:return: tree prjectiviser
		"""

		vertexes = tree.get_vertices()
		proj_bool = False # True si l'arbre à subit un changement
		proj_end = False # False tant que l'arbre n'as pas était passer une fois avec succés 
		
		while not proj_end: # On repasse tant que l'arbre n'est pas projectif
			proj_end = True
			
			for i, vertex in enumerate(vertexes):  # all vertex in tree

				link_list = vertex.get_nodes()

				for indice, link in enumerate(link_list): # Pour tout les arcs partant de vertex
					target = link.target
					
					# Calcule des éléments entre GOV et TARGET
					if vertex.get_index () < target.get_index (): # Si l'arcs part vers la droite
						middle = list (range (vertex.get_index (), target.get_index () + 1))
					elif vertex.get_index () > target.get_index (): # Si l'arcs part vers la gauche
						middle = list (range ( vertex.get_index (),target.get_index () - 1, -1))
					else: # Cas normalement impossible
						print("Projectivité : Un vertex à un lien vers lui même !")
					
					middle = np.asarray(middle)
					
					#print("GOV = ",vertex.get_index(),"TARGET = ",target.get_index ()," Middle=", middle)   
					
					sous_arbre = tree.return_sous_arbre(vertex.get_index())
					#print("Sous arbre de ",vertex.get_index()," : ",sous_arbre)
					
					# Extraction des éléments du sous arbre qui ne sons pas au millieu de GOV et TARGET
					intersect = np.intersect1d(sous_arbre,middle)
					#print("Inter : ",intersect)
					
					# Si il exist des sommet de middle qui ne sont pas dans le sous arbre de GOV
					#print(len(intersect)," ", len(middle))
					if len(intersect) != len(middle):
						# Arc non projectif 
						parent_GOV = vertex.get_parent()
						
						# Récuppération des labels qui seront fusionner
						label = link.label
						label_parent = parent_GOV.get_link_dep(vertex).get_label()
						new_label = label_parent +"|"+ label
						w = target.word.setFeat("LABEL",new_label)
						#print("Nouveau label ",new_label)
						
						# Changer le pére de TARGET
						target.set_parent(parent_GOV)
						
						# Ajouter un lien du père de GOV ver TARGET
						link = Liaison(target,label=new_label)
						parent_GOV.add_link(link)
						
						# Supprimer le lien de GOV vers TARGET
						vertex.delete_link_dep(target)
						
						proj_bool = True
						proj_end = False
				
				
				
				"""for mid in middle[1:-1]: # Pour tout les sommets entre le début et la fin de link
					print("Mid ",mid)
					v = tree.index_search(mid)
					v_gouv = v.get_parent()

					########################################## Sommet Entrant  dans middle###############################################################"

					if (v.get_parent() is not None):
						v_gouv_index = v.parent.get_index()


						if (v_gouv_index not in middle and (vertex.get_word() != target.get_word())):  # corrige le int()
							# print("nOT ", middle, " ", vertex.get_labelWord(), "->", target.get_labelWord(), v_gouv_index, ":",
							#       v.get_labelWord())
							v_gouv_gouv = v_gouv.get_parent()
							if (v_gouv_gouv is not None):
								l_liste = v_gouv_gouv.get_nodes()

								for l in l_liste:
									if (l.target.get_index() == v_gouv_index and v_gouv.get_link_dep(v) is not None):
										link_dep = v_gouv.get_link_dep(v).label  # y
										link_gouv_gouv = l.label  # x
										label = link_gouv_gouv + "|" + link_dep
										# print("label =", label)
										tree.create_link_vertex(v_gouv_gouv, label, v)
										v_gouv.delete_link_dep(v)
										proj_bool = True


				########################################## Sommet Sortant  dans middle###############################################################"

					v = tree.index_search(mid)
					v_all_nodes = v.get_nodes()
					print("vertex = ",vertex.get_word().getFeat("FORM")," Link=",link.label)
					for vt in v_all_nodes:
						print (" V=",v.get_word().getFeat("FORM"),"B = ", vt.target.get_word ().getFeat("FORM"))
						vertex_dep =  vt.target
						vertex_dep_index = int(vt.target.get_word().getFeat("INDEX"))
						#print("INDEX = ",vertex_dep_index ," Middle=", middle)
						print(int(vertex_dep_index) not in middle)
						if (vertex_dep_index not in middle and (vertex.get_word () != target.get_word ())):
							v_link_gouv = v.get_parent()
							v_link_dep =  vt
							link_dep = v_link_gouv.get_link_dep (v).label  # y
							link_gouv_gouv = v_link_dep.label  # x
							label = link_gouv_gouv + "|" + link_dep

							print("label =", label," V=",v.get_word().getFeat("FORM"))
							print(v_link_gouv.get_word().getFeat("FORM"),"....",v_link_dep.target.get_word().getFeat("FORM")," = ",label)
							tree.create_link_vertex (v_link_gouv, label, v_link_dep.target)
							v.delete_link_dep (v_link_dep)
							proj_bool = True
							break




		# print("########## =",proj_bool)
		"""
		return tree,proj_bool


	def deprojectiviser(self,tree):
		"""


		:param tree: Object tree
		:return:

		"""
		dep_proj_exist = False
		vertexes = tree.vertices

		for i, vertex in enumerate(vertexes):

			liste_dep = vertex.get_all_deproj_link()
			for id,dp in enumerate(liste_dep):

				vertex_dep = dp.target

				label = dp.label.split("|")

				x = label[0]
				y = label[1]
				vertex_x = vertex.get_link_dep_by_label(x)

				tree.create_link_vertex(vertex_x.target, y, vertex_dep)
				vertex.delete_link_dep(vertex_dep)

				dep_proj_exist = True

		return tree, dep_proj_exist











if(__name__ == "__main__"):

	"""
	sommet = ["1","2","3","4"]
	arcs = ["1-3","4-2","3-4"]
	arc_labels = ["h","y","x"]
	"""

	sommet = ["l'", "histoire", "dont", "je", "connais", "la", "fin", "."]
	arcs = ["histoire-l'", "histoire-.", "histoire-connais", "fin-dont", "connais-je", "connais-fin", "fin-la"]
	arc_labels = ["a", "b", "c", "deepred", "d", "obj", "f"]


	# tree.push(root)

	def create_tree(sommet, arcs, arc_labels):
		tree = Tree()
		root = Vertex("Root", 0, None, list())

		for index, word in enumerate(sommet):
			if (index == 0):
				tree.push(Vertex(word, index, root, list()))
			else:
				tree.push(Vertex(word, index, None, list()))

		for index, word in enumerate(arcs):
			word = word.split("-")
			print(word)
			tree.link(word[0], arc_labels[index], word[1])

		return tree


	tree = create_tree(sommet,arcs,arc_labels)
	print("#######################################")


	pp =Projectivite()

	t,exist = pp.projectiviser(tree)



	print(t.print_tree())



	dp,exist = pp.deprojectiviser(t)



	print(dp.print_tree())
