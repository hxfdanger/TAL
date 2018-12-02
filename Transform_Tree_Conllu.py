
from Main import  *
from ConstructAllTree import  ConstructAllTree
"""
Classe qui va prendre en paramètre un tree et constuire sont fichier 

"""

class TransformTreeConllu:

    def __init__(self,alltree,filename="generate_data.conllu",file_test = "" ):
        self.alltree = alltree
        self.filename = filename
        self.file_test =file_test
        if(file_test==""):
            self.construct = True
        else:
            self.construct = False
        self.file_test = file_test
        self.file = open(self.filename,"w")
        self.generate()
        self.file.close()


    def get_vertices_mcd(self,vertice):
        """

        :param word:
        :return:
        """


        word = vertice.get_word()
        ligne = ""

        for index,mcd in enumerate(get_mcd()):
            print(vertice.get_word().getFeat("FORM"))
            mcd = mcd[0]
            if(mcd != "GOV" and mcd != "LABEL"):

                if(index < len(get_mcd()) -1):
                     ligne += str(word.getFeat(mcd))+"  "
                else:
                    ligne+=str (word.getFeat (mcd))

            elif(mcd == "GOV"):

                print(vertice.get_parent())
                ligne += str(vertice.get_parent().get_word().getFeat("INDEX"))+"  "

            elif(mcd == "LABEL"):
                parent = vertice.get_parent()
                label = str(parent.get_link_dep(vertice).get_label())
                ligne += label+"  "




        return ligne













    def get_Label(self):
        """

        :return:
        """




    def generate(self):
        """

        :return: file conllu
        """
        if(self.construct == True):

            for index,tree in enumerate(self.alltree):# pour chaque apres

                vertices = tree.get_vertices()
                print(len(vertices))
                ligne_index = "# sent_id = fr-ud-"+str(index)+"\n"
                self.file.writelines (ligne_index)

                self.file.writelines ("#\n")


                for vertice in vertices[1:]:
                    ligne = ""
                    if(self.construct == True):
                         ligne_mcd = self.get_vertices_mcd(vertice)
                    ligne = ligne_mcd
                    self.file.writelines (ligne+"\n")

                if(index < len(self.alltree)):
                     self.file.writelines("\n")

        else:


            conlluFilename=self.file_test
            try:
                conlluFile=open (conlluFilename, encoding='utf-8')
            except IOError:
                print ("erreur ouverture fichier", conlluFilename)
                exit (1)

            s=conlluFile.read ()
            conlluFile.close ()
            # création d'une liste contenant tout les ligne du fichier
            liste_lignes=s.splitlines ()
            indice_tree = 0
            tree = False
            index_vertice = 1



            for ligne in liste_lignes:

                if (len (ligne) == 0):
                    self.file.writelines ("\n")
                    tree=False
                    index_vertice=1
                    indice_tree+=1
                    next

                elif (ligne[0] == "#"):  # Si la ligne est un commentaire
                    self.file.writelines(ligne+"\n")  # separation de la phrase en liste qui respecter normalement
                    tree = True
                    index_vertice = 1
                elif(ligne[0] == " "):
                    tree=False
                    index_vertice = 1
                    indice_tree += 1
                else :


                    print(ligne)
                    tokens=ligne.split ("\t")
                    if '-' not in tokens[0]:
                        print("Taille du graphe=",len(self.alltree)," Graphe=",indice_tree," Vertices=",index_vertice)
                        parent=self.alltree[indice_tree].get_vertices()[index_vertice].get_parent()
                        vertice = self.alltree[indice_tree].get_vertices()[index_vertice]
                        gouv = parent.get_word().getFeat("INDEX")

                        tokens[6]  = str(gouv)+"  "

                        label=str (parent.get_link_dep (vertice).get_label ())

                        tokens[7] =  label+"  "
                        ligne = ""
                        for tok in tokens:
                            ligne += tok+"  "

                        self.file.writelines (ligne+"\n")
                        index_vertice+=1

                        tree=False




if(__name__ == "__main__"):


    obj_generateAlltree=ConstructAllTree ("Data/fr_gsd-ud-tr.conllu", get_mcd(), False)
    all_tree=obj_generateAlltree.get_allTree()

    print(len(all_tree))
    file_genarate = TransformTreeConllu(all_tree,"generate_data.txt","Data/fr_gsd-ud-tr.conllu")

    # print(all_tree[0].print_tree())

    ligne = ""
    for t in range(10):
        ligne += str(t)+"  "
    print(ligne)
    # t = "5-5"
    # print('-'  in t)



