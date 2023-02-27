import pandas as pd
from math import log2
from classes.Noeud import Noeud
from classes.Arbre import Arbre


def trouver_premier_attribut (df, nom_colonne_classes) :
    total = len(df)
    classes = trouver_classes(df, nom_colonne_classes)
    attributs = list(df.columns)
    attributs.remove(nom_colonne_classes)
    entropie_dataset = calcul_entropie_dataset(df, nom_colonne_classes)


    entropies = [0]*len(attributs)
    occurences_totales = {}

    for i in attributs :
        classes_attributs = trouver_classes(df, i)
        #print(classes)
        occurences = {}
        for j in classes_attributs :
            occurences[j] = [0]*len(classes)
        # print(occurences)
        for k in range (len(df)) :
            # print(nom_colonne_classes, k, df[nom_colonne_classes][k])
            valeur = df[i][k]
            # print(valeur)
            if df[nom_colonne_classes][k] == 'No' :
                occurences[valeur][0] += 1
            else : occurences[valeur][1] += 1
        #print(occurences)
        occurences_totales[i] = occurences
    
    #print(occurences_totales)
    
    

    for i in enumerate(list(occurences_totales.keys())) :
        entropie_variable = entropie_dataset
        #print(i[0], i[1])
        for j in list(occurences_totales[i[1]].keys()) :
            #print(j)
            v1 = occurences_totales[i[1]][j][0]
            v2 = occurences_totales[i[1]][j][1]
            if v1 == 0.0 :
                v1 = 0.000001
            if v2 == 0.0 :
                v2 = 0.000001  

            entropie_variable -= ((v1+v2)/total)*(-v1/(v1+v2)*log2(v1/(v1+v2)) - v2/(v1+v2)*log2(v2/(v1+v2)))
        
        entropies[i[0]] = entropie_variable

    resultat = attributs[entropies.index(max(entropies))]
    return resultat, list(occurences_totales[resultat].keys())


def initialiser_arbre (df, nom_colonne_classes, colonnes_a_retirer = None) :
    if colonnes_a_retirer != None :
        for i in colonnes_a_retirer :
            df = df.drop(i, axis=1)
    #print(df)
    racine, enfants = trouver_premier_attribut(df, nom_colonne_classes)
    print(racine, enfants)

    arbre = Arbre(Noeud(racine))
    for i in enfants : 
        arbre.racine.ajouter_enfant(i)
    return arbre



def calcul_entropie_dataset (df, colonne_classe) :
    classes = trouver_classes(df, str(list(df.columns)[-1]))
    occurences = [0]*len(classes)
    # classe = str(list(df.columns)[-1])
    classe = colonne_classe
    for i in df[classe] :
        index = classes.index(i)
        occurences[index] += 1

    longueur = len(df)
    resultat = 0
    for i in occurences :
        resultat += -i/longueur * log2(i/longueur)
    #print(resultat)
    return resultat


def trouver_classes (df, nom_colonne) :
    index = df.columns.get_loc(nom_colonne)
    classe = str(list(df.columns)[index])
    liste = []
    for i in df[classe] :
        if i not in liste :
            liste.append(i)
    return liste


def main (lien_data, colonne_classes, colonnes_a_supprimer) :
    print("\n")
    df = pd.read_csv(lien_data)
    initialiser_arbre(df, colonne_classes, colonnes_a_supprimer)
    print("\n")


### MAIN ### 

if __name__ == "__main__" :
    main("data/tennis.csv", "play", ['day'])