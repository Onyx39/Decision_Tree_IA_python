"""
Classe "Noeud", représente les noeuds de l'arbre
"""

class Noeud :
    """
    Implémentation de la classe "Noeud".
    Paramètres :
        nom (str) : label du noeud
        enfants (liste) : liste des enfants du noeud (défaut : [])
        attribut_suivant : ***** (defaut : None)
        valeur : **** (defaut : None)
    """
    def __init__(self, nom, enfants = None, attribut_suivant = None, valeur = None) :
        self.nom = nom
        self.enfants = enfants
        self.attribut_suivant = attribut_suivant
        self.valeur = valeur

    def __str__ (self) :
        return self.nom

    def ajouter_enfant (self, nom) :
        """
        Méthode pour ajouter un enfant à un noeud
        Paramètre :
            nom (str) : nom du noeud enfant

        Retour :
            self
        """
        if self.enfants is None :
            self.enfants = [Noeud(nom, enfants=[])]
            return self
        self.enfants.append(Noeud(nom, enfants=[]))
        return self

    def set_valeur (self, new_valeur) :
        """
        Méthode pour définir la valeur associée à un noeud
        Paramètre :
            new_valeur (float) : nouvelle valeur

        Retour :
            self
        """
        self.valeur = new_valeur
        return self

    def set_attribut_suivant (self, new_valeur) :
        """
        Méthode pour définir l'attribut suivant associé à un noeud
        Paramètre :
            new_valeur (str) : nouvel attribut

        Retour :
            self
        """
        self.attribut_suivant = new_valeur
        return self

    def chercher_sous_arbre(self, label) :
        """
        Recherche un noeud possèdant un label dans la descendance du noeud
        Paramètre :
            label (str) : le label recherché

        Retour :
            noeud (Noeud) ou None
        """
        #print(self)
        # if self.nom == label :
        #     return self
        # for i in self.enfants :
        #     y = i.chercher_sous_arbre(label)
        #     if y :
        #         break
        # return None

        s_list = []
        if self.nom is label:
            return self
        s_list.extend(self.enfants)
        while s_list:
            noeud = s_list.pop()
            if noeud.nom is label :
                return noeud
            s_list.extend(noeud.enfants)
        return None
        # if self.nom == label:
        #     print(self.nom)
        #     return self
        # else:
        #     y = None
        #     for i in self.enfants :
        #         y = i.chercher_sous_arbre(label)
        #         if y:
        #             break
        # return None
