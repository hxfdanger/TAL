
from automate import *

class Projectivite:






    def projectiviser(self,tree):
        """

        :param tree: Object tree
        :return: tree prjectiviser
        """
        vertexes = tree.vertices

        for i, vertex in enumerate(vertexes): # all vertex in tree

            indice, word = vertex.get_index(), vertex.get_word()
            link_list = vertex.get_nodes()
            proj_bool = False
            for indice, link in enumerate(link_list):
                target = link.target

                middle = list(range(vertex.get_index(), target.get_index() + 1))
                for mid in middle:
                    v = tree.index_search(mid)
                    v_gouv = v.parent
                    if(v.parent  is not None):
                            v_gouv_index = v.parent.get_index()
                            if (v_gouv_index not in middle and (vertex.get_word() != target.get_word())):  # corrige le int()
                                print("nOT ", middle, " ", vertex.get_word(), "->", target.get_word(), v_gouv_index, ":",
                                      v.get_word())
                                v_gouv_gouv = v_gouv.parent
                                if (v_gouv_gouv is not None):
                                        l_liste = v_gouv_gouv.get_nodes()

                                        for l in l_liste:
                                            if (l.target.get_index() == v_gouv_index):
                                                link_dep = v_gouv.get_link_dep(v).label  # y
                                                link_gouv_gouv = l.label  # x
                                                label = link_gouv_gouv + "|" + link_dep
                                                print("label =", label)
                                                tree.create_link_vertex(v_gouv_gouv, label, v)
                                                v_gouv.delete_link_dep(v)
                                                print(v_gouv.nodes)
                                                proj_bool = True


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











"""
sommet = ["1","2","3","4"]
arcs = ["1-3","4-2","3-4"]
arc_labels = ["h","y","x"]
"""

sommet = ["l'","histoire","dont","je","connais","la","fin","."]
arcs = ["histoire-l'","histoire-.","histoire-connais","fin-dont","connais-je","connais-fin","fin-la"]
arc_labels = ["a","b","c","deepred","d","obj","f"]




#tree.push(root)

def create_tree(sommet,arcs,arc_labels):
        tree = Tree()
        root = Vertex("Root", 0, None, list())

        for  index,word in enumerate(sommet):
                if(index == 0):
                   tree.push(Vertex(word,index,root,list()))
                else:
                    tree.push(Vertex(word, index, None, list()))


        for  index,word in enumerate(arcs):
             word = word.split("-")
             print(word)
             tree.link(word[0],arc_labels[index],word[1])

        return tree



tree = create_tree(sommet,arcs,arc_labels)
print("#######################################")


pp =Projectivite()

t,exist = pp.projectiviser(tree)

print("######################### Projectiviser ##################################")
print(t)

print(t.print_tree())



dp,exist = pp.deprojectiviser(t)

print("####################  DProjective ##########################")


print(dp.print_tree())