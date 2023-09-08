"""
Classe "Arbre", représente l'arbre de décision construit
"""

class Arbre :
    """
    Implémentation de la classe "Arbre".
    Paramètre :
        racine (Noeud) : racine de l'Arbre
    """
    def __init__(self, racine) :
        self.racine = racine

    def __str__ (self) :
        return str(self.racine.nom)

    def chercher(self, label) :
        """
        Recherche un noeud possèdant un label dans l'Arbre
        Paramètre :
            label (str) : le label recherché

        Retour :
            noeud (Noeud) ou None
        """
        return self.racine.chercher_sous_arbre(label)
