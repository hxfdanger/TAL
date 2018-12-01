import sys
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import OneHotEncoder
from keras.utils.np_utils import to_categorical
from util import get_coefs_word


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
        nb_form = 0  # Compte le nombre de features de type FORM

        self.names = list()

        # Lecture du fichier
        with open(features_file, 'r') as f:
            lines = f.readlines()
        # Remplissage des noms
        for line in lines:
            line = line.split(".")
            line[-1] = line[-1].rstrip('\n')

            if line[0] == 'S':
                idx = int(line[1])
                feat = line[2]
                self.names.append(("Pile", idx, feat))
                if feat == 'FORM':
                    nb_form += 1
            elif line[0] == 'B':
                idx = int(line[1])
                feat = line[2]
                self.names.append(("Buffer", idx, feat))
                if feat == 'FORM':
                    nb_form += 1
            else:
                self.names.append(line[0])
        print("Features prise en compte : ", self.names)

        # Dataset
        self.nb_form = nb_form
        self.forms = list()  # Liste des mots du dataset avant leurs embedding
        self.datas = list()
        self.labels = list()

        # Labels encoders pour crée les vecteurs one hot du dataset
        self.labels_encoders = list()
        for features in self.names:
            if features[2] != 'FORM':
                self.labels_encoders.append(LabelEncoder())
        # Label encoder pour crée les vecteurs one hot des labels
        self.label_encoder_Y = LabelEncoder()

    def extract_features(self, pile, buff, tree):
        """
        input:
                                        pile = La pile courante
                                        buff = Le buffer courant
                                        tree = L'arbre courant
        Extrait les features de l'état courant (pile,buff,tree) et les
        ajoute à self.datas
        """
        data = list()  # Liste des features de l'états courant
        form = list()  # Liste des mots en clair

        for feature in self.names:  #  Pour toutes les features connues
            # print(feature)

            if feature[0] == 'Pile':  # Si la feature concerne la pile
                idx = feature[1]
                feat = feature[2]
                idx_pile = pile.see(idx)
                if idx_pile != None:
                    if feat == 'FORM':  # Si il sagit d'un mot
                        form.append(
                            tree.vertices[idx_pile].get_elementWord(element=feat))
                    else:
                        data.append(
                            tree.vertices[idx_pile].get_elementWord(element=feat))

                    # print(data)
                else:
                    if feat == 'FORM':  # Si il sagit d'un mot
                        form.append('NA')  # Donnée non aquise
                    else:
                        data.append('NA')  # Donnée non aquise

            elif feature[0] == 'Buffer':  # Si la feature concerne le buffer
                idx_buff = feature[1]
                feat = feature[2]

                idx = buff.see(0)
                if idx == None:  # Si le buffer est vide on ce place juste après le dernier mot
                    idx = len(tree.vertices)

                # Si la features concerne un élément hors de la phrase
                if idx + idx_buff < 0 or idx + idx_buff >= len(tree.vertices):
                    if feat == 'FORM':  # Si il sagit d'un mot
                        form.append('NA')  # Donnée non aquise
                    else:
                        data.append('NA')  # Donnée non aquise
                else:
                    if feat == 'FORM':  # Si il sagit d'un mot
                        form.append(
                            tree.vertices[idx + idx_buff].get_elementWord(element=feat))
                    else:
                        data.append(
                            tree.vertices[idx + idx_buff].get_elementWord(element=feat))

            elif feature == 'DIST':  # Si la feature est une distance
                Spile = pile.see(0)
                Sbuff = buff.see(0)
                if Spile != None and Sbuff != None:
                    data.append(
                        abs(tree.vertices[Spile].get_index() - tree.vertices[Sbuff].get_index()))
                else:
                    data.append('NA')  # Donnée non aquise

        if len(form) > 0:
            self.forms.append(form)
        self.datas.append(data)

        # print(data)
        return data

    def convert_data_to_one_hot(self, data):
        """
        Converti la liste de features data en un tableau 1D de vecteur one hot
        """
        if len(data) != len(self.names) - self.nb_form:
            print("La donnée ne posséde pas autant de features que demander !")
            return None

        # print(data)
        new_data = list()  # Liste des vecteurs one hot de data
        for i, feature in enumerate(data):
            feature = np.array(feature).reshape(1,)  # Shape pour le transform

            feature = self.labels_encoders[i].transform(feature)
            feature = to_categorical(feature, len(
                self.labels_encoders[i].classes_))

            feature = np.array(feature).reshape(-1,)  # Annulation du shape

            new_data.append(feature)
            # print(new_data[-1])

        # print(new_data)
        return new_data.copy()

    def convert_datas_to_one_hot(self):
        """
        Entrainent les labels encoders sur le dataset
        Converti les self.datas en un vecteur one hot
        """
        if len(self.datas) <= 0:
            print(
                "Le dataset est vide, il est impossible d'entrainer les labels encoders!")
            return None

        # Entrainment des labels_encoders
        values = np.array(self.datas)
        # print(values.shape)

        for i, encoder in enumerate(self.labels_encoders):
            # print(values[:,i])
            encoder = encoder.fit(values[:, i])

        X_data = []
        # Convertion du dataset
        for data in self.datas:
            X = self.convert_data_to_one_hot(data)
            # print(X)

            # Applatissement du vecteur X
            X1 = np.array(X[0])
            for i in range(0, len(X)):
                X1 = np.concatenate((X1, X[i]), axis=None)

            X_data.append(X1)

        X_data = np.asarray(X_data)
        return X_data

    def convert_labels_to_one_hot(self):
        """
        Entrainent le labels encoders sur le dataset
        Converti les self.labels en un vecteur one hot
        """
        if len(self.labels) <= 0:
            print(
                "Les labels sont vide, il est impossible d'entrainer les labels encoders!")
            return None

        # Entrainment du labels_encoders
        values = np.array(self.labels)
        # print(values)

        # Entrainement du label_encoder_Y
        self.label_encoder = self.label_encoder_Y.fit(values)

        Y_data = []
        # Convertion des labels
        for label in self.labels:
            label = np.array(label).reshape(1,)  # Shape pour le transform

            label = self.label_encoder_Y.transform(label)
            label = to_categorical(label, len(self.label_encoder.classes_))

            label = np.array(label).reshape(-1,)  # Annulation du shape
            # print(label)
            Y_data.append(label)

        Y_data = np.asarray(Y_data)
        return Y_data

    def nombre_labels(self):
        """
        Renvoie le nombre de labels differents possible
        """
        return len(self.label_encoder_Y.classes_)

    def inverse_onehot_label(self, label):
        """
        Renvoie le label corespondant au label sous forme de one hot
        """
        # reverse to_categorical
        label = np.argmax(label, axis=0)
        label = np.array(label).reshape(1,)  # Shape pour le transform

        # reverse LabelEncoder
        label = self.label_encoder_Y.inverse_transform(label)

        return label

    def convert_forms_to_embedding(self, path_embed):
        """
        Convertie les mots de forms en utlisant l'embedding
                path_embed : Le chemin vers le fichier d'embedding
        """
        forms_data = []
        for x in self.forms:
            coefs = []
            for word in x:
                vec = get_coefs_word(word, path_embed, dim_coefs=100)
                coefs.append(vec)

            coefs = np.array(coefs)
            coefs = coefs.flatten()
            forms_data.append(coefs)

        X = np.asarray(forms_data)
        return X

    def get_Data_Set(self, file_embedding=None):
        onehot_X = self.convert_datas_to_one_hot()
        # print("Final X ", onehot_X)
        onehot_Y = self.convert_labels_to_one_hot()
        # print("Final Y ", onehot_Y)
        X = onehot_X
        if(file_embedding is not None):
            words = self.convert_forms_to_embedding(file_embedding)
            X = np.column_stack((words, onehot_X))

        return X, onehot_Y


# Pour faire des One-hot
# https://machinelearningmastery.com/how-to-one-hot-encode-sequence-data-in-python/


if(__name__ == "__main__"):
    features = Features("Data/f3_tbp.fm")
