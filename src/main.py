"""
Fichier principal, exécutable
"""

from math import log2

import pandas as pd

from classes.arbre import Arbre
from classes.noeud import Noeud

def trouver_premier_attribut (dataframe, nom_colonne_classes) :
    """
    Trouver le premier attribut pour séparer les données
    Paramètres :
        ...

    Retour :
        ...
    """
    classes = trouver_classes(dataframe, nom_colonne_classes)
    attributs = list(dataframe.columns)
    attributs.remove(nom_colonne_classes)
    entropie_dataset = calcul_entropie_dataset(dataframe, nom_colonne_classes)


    entropies = [0]*len(attributs)
    occurences_totales = {}

    for i in attributs :
        classes_attributs = trouver_classes(dataframe, i)
        occurences = {}
        for j in classes_attributs :
            occurences[j] = [0]*len(classes)
        # print(occurences)
        # print(len(dataframe))
        for k in range (len(dataframe)) :
            # print(nom_colonne_classes, k, dataframe[nom_colonne_classes][k])
            # print(i, k)
            # print(list(dataframe.index))
            valeur = dataframe[i][list(dataframe.index)[k]]
            # print(valeur)
            valeur_classe = dataframe[nom_colonne_classes][list(dataframe.index)[k]]
            for classe in enumerate(classes) :
                if classe[1] == valeur_classe :
                    occurences[valeur][classe[0]] += 1
        #print(occurences)
        occurences_totales[i] = occurences

    #print(occurences_totales)



    for i in enumerate(list(occurences_totales.keys())) :
        entropie_variable = entropie_dataset
        #print(i[0], i[1])
        for j in list(occurences_totales[i[1]].keys()) :
            liste_occurences = occurences_totales[i[1]][j]
            somme = sum(liste_occurences)
            for k in enumerate(liste_occurences) :
                somme_entropies = 0
                occurence = liste_occurences[k[0]]
                if occurence == 0 :
                    occurence = 0.0000001
                somme_entropies -= (-occurence/somme)*log2(occurence/somme)

            entropie_variable += somme_entropies*(somme/len(dataframe))

            # v1 = occurences_totales[i[1]][j][0]
            # v2 = occurences_totales[i[1]][j][1]
            # if v1 == 0.0 :
            #     v1 = 0.000001
            # if v2 == 0.0 :
            #     v2 = 0.000001

            # v = v1 + v2
            # entropie_variable -= ((v)/total)*(-v1/(v)*log2(v1/(v)) - v2/(v)*log2(v2/(v)))

        entropies[i[0]] = entropie_variable

    resultat = attributs[entropies.index(max(entropies))]
    # print(resultat, entropies)
    return resultat, list(occurences_totales[resultat].keys())


def initialiser_arbre (dataframe, nom_colonne_classes, colonnes_a_retirer = None) :
    """
    Initialise l'arbre de décision
    Paramètres :
        dataframe (pd.df) : le jeu de données
        nom_colonnes_classes (liste) : liste contenant les attributs à traiter
        colonnes_a_retirer (liste | None) :  les colonnes à ne pas prendre en compte
    """
    if not colonnes_a_retirer is None :
        for i in colonnes_a_retirer :
            dataframe = dataframe.drop(i, axis=1)
    #print(dataframe)
    racine, enfants = trouver_premier_attribut(dataframe, nom_colonne_classes)
    print(racine, enfants)

    arbre = Arbre(Noeud(racine))
    for enfant in enfants :
        arbre.racine.ajouter_enfant(enfant)

    # print(arbre)
    # print(arbre.racine)
    # print(len(arbre.racine.enfants))
    # print(len(arbre.racine.enfants[0].enfants))

    truc = split_dataset(dataframe, arbre.racine)
    traiter_subsets(truc, nom_colonne_classes, arbre)

    return arbre

def split_dataset (dataframe, noeud) :
    """
    Sépare le dataset en fonction du label d'un noeud
    Paramètres :
        dataframe (pd.df) : le jeu de données
        noeud (Noeud) : le noeud qui contient le label

    Retour :
        res (liste) : liste de datasets
    """
    res = []
    grouped = dataframe.groupby(dataframe[noeud.nom])
    for i in grouped :
        res.append(i)
    # print(res, len(res), len(res[0]), res[0][0])
    return res

def traiter_subsets (liste_subset, nom_colonne, arbre) :
    """
    Traite un sous dataset
    Paramètres :
        ...

    Retour :
        ...
    """
    for i in liste_subset :
        classes = trouver_classes(i[1], nom_colonne)
        if len(classes) == 1 :
            for j in arbre.racine.enfants :
                #print(i)
                if j.nom == i[0] :
                    j.set_valeur(i[1][nom_colonne].iloc[0])
                    # print(j.valeur)
        else :
            longueur = len(i[1])
            frequences = [0]*len(classes)
            for j in i[1][nom_colonne] :
                for classe in enumerate(classes) :
                    if classe[1] == j :
                        frequences[classe[0]] += 1

            for k in enumerate(frequences) :
                frequences[k[0]] = frequences[k[0]]/longueur
            print("___", i[0], frequences)

            #print(i[1])
            new_attribut = trouver_premier_attribut(i[1], nom_colonne)
            print(new_attribut, i[0])
            parent = arbre.chercher(i[0])
            print(parent)
            for attribut in new_attribut[1] :
                parent.ajouter_enfant(Noeud(attribut))
            #print("---------", arbre.chercher(str(i[0])))


            # for j in arbre.racine.enfants :
            #     if j.nom == i[0] :
            #         for k in new_attribut[1] :
            #             j.ajouter_enfant(Noeud(k))
            #         break
            #     break



    print('kj f')
    print(arbre.racine.enfants[0].nom)
    for enfant in arbre.racine.enfants[0].enfants :
        print(enfant.nom)
    print(len(arbre.racine.enfants[0].enfants ))

    print(arbre.racine.enfants[1].nom)
    for enfant in arbre.racine.enfants[1].enfants :
        print(enfant.nom)
    print(len(arbre.racine.enfants[1].enfants ))

    print(arbre.racine.enfants[2].nom)
    for enfant in arbre.racine.enfants[2].enfants :
        print(enfant.nom)
    print(len(arbre.racine.enfants[2].enfants ))








def calcul_entropie_dataset (dataframe, colonne_classe) :
    """
    Calcule l'entropie du dataset
    Paramètres :
        dataframe (pd.df) : le jeu de données
        colonne_classe (str) : le nom de la colonne "résultat"

    Retour :
        resultat (float) : l'entropie du dataset
    """
    classes = trouver_classes(dataframe, str(list(dataframe.columns)[-1]))
    occurences = [0]*len(classes)
    # classe = str(list(dataframe.columns)[-1])
    classe = colonne_classe
    for i in dataframe[classe] :
        index = classes.index(i)
        occurences[index] += 1

    longueur = len(dataframe)
    resultat = 0
    for i in occurences :
        resultat += -i/longueur * log2(i/longueur)
    #print(resultat)
    return resultat


def trouver_classes (dataframe, nom_colonne) :
    """
    Trouver les différentes classes de résultats
    Paramètres :
        ...

    Retour :
        ...
    """
    index = dataframe.columns.get_loc(nom_colonne)
    classe = str(list(dataframe.columns)[index])
    liste = []
    for i in dataframe[classe] :
        if i not in liste :
            liste.append(i)
    return liste


def main (lien_data, colonne_classes, colonnes_a_supprimer) :
    """
    Fonction principale, fait tourner l'algorithme
    Paramètres :
        lien_data (str) : le lien vers les données
        colonne_classes (str) : le nom de la colonne "résultat"
        colonnes_a_supprimer (liste) : les colonnes à ne pas prendre en compte

    Aucun retour
    """
    print("\n")
    dataframe = pd.read_csv(lien_data)
    initialiser_arbre(dataframe, colonne_classes, colonnes_a_supprimer)
    print("\n")


### MAIN ###

if __name__ == "__main__" :
    main("data/tennis.csv", "play", ['day'])
    # n = Noeud('racine')
    # n.ajouter_enfant('fils')
    # print(n)
    # print(n.enfants)
    # print(n.enfants[0])
    # print(n.enfants[0].enfants)
