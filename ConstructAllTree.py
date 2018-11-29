from arbre import Vertex,Tree,Liaison
from Word import Word
from  Projectivite import Projectivite


# TODO : genere une premier jeu de données d'entrainement pour le reseau avec Dicos


class ConstructAllTree:

    """
    Objectif de cette classe est de créer des structure arborecense pour chaque phrase
    ceci nous facilitera la gestion et

    """

    __author__ =    "ibrahim souleiman"



    def __init__(self,filename,mcd,projectivser = False):
        """

        :param filename: Nom du fichier
        :param mcd: liste tuple contenant  tout les champs de chaque ligne
        """
        self.filename = filename
        self.mcd = mcd
        self.alltree = []
        self.link_not_create = [] # liste des contenant lien qui ne sont pas encore créer
        self.generate_tree()
        self.alltreeProjectivise = []

        if(projectivser):

            obj_proj = Projectivite()

            for tree in self.alltree:
                # tree.print_tree()

                proj_tree, exist = obj_proj.projectiviser(tree)
                # print("Exist Proj=",exist)

                if (exist == True): # projectivse l'arbre qui deprojectivser
                    # proj_tree.print_tree()
                    # print("####################### Projectiviser ################")
                    # print(proj_tree.print_tree())
                    self.alltreeProjectivise.append(proj_tree)
                else:

                    self.alltreeProjectivise.append(tree)








    def get_allTree(self):
        return self.alltree

    def get_allTreeProjectiviser(self):
        return self.alltreeProjectivise



    def verify_add_newLink(self,tree,word_actual):
        """
        Methode permettons de créer le lien mis de côte (c'est a dire lorsque on parcourir lineairement les fichier
        certaint mot peuvent avoir pour gouvernement de mot present plus bas pour ne pas a chaque fois parcourir les mots et trouve le
        gouverneur correspondant, nous avons préfere d'utilise une liste tamporaire contenant le lien qui ne sont pas créer encore et la
        créer une fois l'indice du gouverneur atteint nous créer le lien


        :param tree: instance de classe Tree pour la phrase courante
        :param word_actual: mot actuel
        :return: efface dans la liste l'element dans  le lien a ete créer
        """

        word_index = word_actual.getFeat("INDEX");
        id = -1

        for index,word in enumerate(self.link_not_create):
            if (word.getFeat("GOV") == word_index):
                if(word.getFeat("LABEL") != "-"):
                    w_index = int(word.getFeat("INDEX"))
                    wactual_index = int(word_actual.getFeat("INDEX"))
                    tree.link( wactual_index,word.getFeat("LABEL"),w_index )
                    id  = index

                else:
                    print("Erreur sur le Label")

        if(id != -1):
            del self.link_not_create[id]




    def create_root(self):
        """
        méthode nous permettons de créer un sommet root

        :return:
        """
        w = Word()
        w.setFeat("INDEX", 0)
        w.setFeat("FORM", "root")
        w.setFeat("LEMMA", "root")
        w.setFeat("POS", "root")
        w.setFeat("X1", "root")
        w.setFeat("MORPHO", "root")
        w.setFeat("GOV", "root")
        w.setFeat("LABEL", "root")
        w.setFeat("X2", "root")
        w.setFeat("X3", "root")
        root = Vertex(w, None, list())
        return  root








    def generate_tree(self):
        """

        Méthode qui parcour tout les fichier et nous créer pour chaque phrase sa structure arborescence associé.

        """

        conlluFilename = self.filename
        try:
            conlluFile = open(conlluFilename, encoding='utf-8')
        except IOError:
            exit(1)

        s = conlluFile.read()
        conlluFile.close()
        liste_lignes = s.splitlines() # création d'une liste contenant tout les ligne du fichier



        tree = Tree()

        for index,ligne in enumerate(liste_lignes): # pour chaque ligne du fichier
            root = self.create_root()

            if(len(ligne) == 0): # verification dans le cas ou la ligne est vide
                if (len(tree.get_vertices()) > 0): # si la structure arbre a ete construit pour la précedent phrase
                    self.alltree.append(tree)
                self.link_not_create = list() # réinitlisation de nôtre liste temporaire (stocke le lien qui ne sont pas encore créer) pour chaque nouvelle phrase
                tree = Tree()

                next

            else:
                if(ligne[0] == "#"):
                    tokens = ligne.split() # separation de la phrase en liste qui respecter normalement
                else:
                    tokens = ligne.split("\t") # separation de la phrase en liste qui respecter normalement




                if len(tokens) != len(self.mcd) and tokens[0]!= "#":
                    print("Erreur :  La Taille du fichier mcd n'est pas egal a la taille du cologne de la ligne =",ligne)
                    exit()

                if(tokens[0] == "#"):
                    if(len(tree.get_vertices()) > 0):
                        self.alltree.append(tree)

                    self.link_not_create = list()
                    tree = Tree()

                    next

                if(tokens[0] != "#"):
                    if '-' not in tokens[0]:
                        w = Word()
                        bool_root = False
                        gov_exist = False
                        list_att_link = False
                        gov_index = 0
                        if(int(tokens[0]) == 1):
                           tree.push(root)

                        for i in range(0, len(tokens)):

                            mcd_actual = self.mcd[i][0]

                            if(mcd_actual == "GOV" and tokens[i] != '-'):
                                gov_exist = True
                                gov_index = int(tokens[i])
                            if(mcd_actual == "LABEL" and gov_exist==0):
                                bool_root = True




                            w.setFeat(mcd_actual,tokens[i])

                        w.setFeat('EOS', '0')


                        if (int(w.getFeat("GOV")) < int(w.getFeat("INDEX"))):
                            """
                            Le cas ou le nous avons pas encore construit le gouverneur
                            """
                            list_att_link = True

                        # print(w.getFeat("INDEX")," ",w.getFeat("GOV")," ",list_att_link)



                        if(bool_root):
                            tree.push(Vertex(w, root, list()))
                            wactual_index = int(w.getFeat("INDEX"))
                            root_index = 0 # indice du root est à 0 pour eviter le confusion avec les mot de la phrase qui commence par 1
                            tree.link(root_index, w.getFeat("LABEL"),  wactual_index)


                        else:
                            tree.push(Vertex(w, None, list()))

                            if(list_att_link):
                                """
                       Ajouter directement le lien

                                """
                                wactual_index = int(w.getFeat("INDEX"))
                                gov_index = gov_index

                                tree.link(gov_index, w.getFeat("LABEL") ,wactual_index)


                            else:
                                """
                                                                Ajouter dans la liste

                                """
                                self.link_not_create.append(w)


                    self.verify_add_newLink(tree,w)





                    if (index == len(liste_lignes)-1):
                        self.alltree.append(tree)









if(__name__ == "__main__"):
    mcd = (('INDEX', 'INT'), ('FORM', 'INT'), ('LEMMA', 'INT'), ('POS', 'SYM'), ('X1', 'INT'), ('MORPHO', 'INT'),
           ('GOV', 'SYM'), ('LABEL', 'SYM'), ('X2', 'SYM'), ('X3', 'SYM'))

    obj_generateAlltree = ConstructAllTree("test.txt",mcd,True)


    # all_tree = obj_generateAlltree.get_allTreeProjectiviser()
    #
    #
    # pp =Projectivite()
    #
    # for tree in all_tree:
    #         tree.print_tree()


         # for index, vertice in enumerate(tree.get_vertices()):
         #     if(index > 0):
         #        print(vertice.get_word().getFeat("FORM")," .............",vertice.get_parent().get_labelWord())
         #
