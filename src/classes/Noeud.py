class Noeud :
    def __init__(self, nom, enfants = []):
        self.nom = nom
        self.enfants = enfants 
        
    def __str__ (self) :
        return self.nom
    
    def ajouter_enfant (self, nom):
        self.enfants.append(Noeud(nom))
        return self