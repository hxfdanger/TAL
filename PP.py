
from automate import *




def get_arc_projective(sommets,arc,arc_label):
    """
    :param sommets:
    :param arc:
    :param arc_label:
    :return: arc projectiviser
    """


    """
    
    pour tout sommet:
    arc_max = arg max (sommet) arrets

    arc_sommet = arrets[sommet]

    parcourir arc_sommet:

              arc_nonprojec = []
          
              verifier si il existe un arc qui ne  vient arc_sommet :
                   arc_nonprojec = arc
                   gouv = arc_nonprojec.get_gouv()
                   arc_ver_gouv = trouve_arc(gouv,arc_nonprojec.get_gouv())
                   effacer_arcs(arc_ver_gouv,arc_nonprojec)
                   ajout_arc(gouv,arc_nonprojec.getcible() )
                   ajout-etique(arc_ver_gouv.getlab(),":", arc_nonprojec.getlabel)                  
                   
                   
                   &
                   
                   
                
    """

    for s in range(len(arc)):
        print("arc = ",arc[s])
        gouv = int(arc[s].split("-")[0])
        cible = int(arc[s].split("-")[1])

        if(gouv<cible+1) :
            middle = list(range(gouv , cible+1))
            #print(middle)
            for a in range(len(arc)):
                print(a)
                print("A=",arc[a])
                gouv_inter = int(arc[a].split("-")[0])
                cible_inter = int(arc[a].split("-")[1])
                #print("cible = ",cible_inter," middle=",middle," arc = ",arc[a])
                if((cible_inter in middle and gouv_inter not in middle) and arc[a]!=arc[s]):
                     arc_non_proj = arc[a]
                     gouv_non_proj,label = get_gouv_gouv_non_proj(arc_non_proj,arcs,arc_labels)
                     label_nproj = arc_labels[a]
                     print(gouv_non_proj ," - ",cible_inter ," ",label, " ",arc_labels[a])
                     s = str(gouv_non_proj)+"-"+str(cible_inter)
                     print(s)
                     del arc[a]
                     del arc_labels[a]
                     arc.append(s)
                     arc_labels.append(label+":"+label_nproj)
                     print(arc)
                     print(arc_labels)
                     return 0






def get_gouv_gouv_non_proj(arc,arcs,arc_labels):
    gouv_arc = int(arc.split("-")[0])
    cible_arc = int(arc.split("-")[1])

    gouv = 0

    for i in range(len(arcs)):
        gouv_inter = int(arcs[i].split("-")[0])
        cible_inter = int(arcs[i].split("-")[1])
        if(cible_inter == gouv_arc):
           return gouv_inter , arc_labels[i]


    return gouv , " "





#sentence = ["sami", "va", "à", "la", "école"]


sommet = ["1","2","3","4"]
arcs = ["1-3","4-2","3-4",]
arc_labels = ["h","y","x"]


vertexs = list()
root = Vertex("Root", 0, None, list())


tree = Tree()

vertexes = tree.get_all_vertex()


for  index,word in enumerate(sommet):
        if(index == 0):
           tree.push(Vertex(word,index+1,root,list()))
        else:
            tree.push(Vertex(word, index+1, None, list()))


for  index,word in enumerate(arcs):
     word = word.split("-")
     tree.link(word[0],arc_labels[index],word[1])

print("##############################################")

vertexes = tree.get_all_vertex()
links = tree.get_all_link()

print(links)
"""
pour chaque sommet je vais choisir 

-   le somme entrant , indice
-   sommet sortant ,indice





"""

for i, word in enumerate(vertexes):
    print(word.get_word().get)







#get_arc_projective(sommet,arcs,arc_labels)


class Projectivise:


    def _deprojectvise(self,arbre):
        pass

    def projectivise(self,arbre):
        pass
