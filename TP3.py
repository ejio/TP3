class Noeud:
    def __init__(self, valeur):
        self.valeur = valeur
        self.gauche = None
        self.droite = None

class ArbreBinaire:
    def __init__(self):
        self.racine = None

    def est_vide(self):
        resultat = (self.racine is None)
        return resultat

    def contient(self, valeur):
        courant = self.racine
        trouve = False
        while courant is not None and not trouve:
            if valeur == courant.valeur:
                trouve = True
            elif valeur < courant.valeur:
                courant = courant.gauche
            else:
                courant = courant.droite
        return trouve

    def ajouter(self, valeur):
        nouveau_noeud = Noeud(valeur)
        if self.racine is None:
            self.racine = nouveau_noeud
        else:
            courant = self.racine
            parent = Noeud(None)
            while courant is not None:
                parent = courant
                if valeur < courant.valeur:
                    courant = courant.gauche
                else:
                    courant = courant.droite
            if valeur < parent.valeur:
                parent.gauche = nouveau_noeud
            else:
                parent.droite = nouveau_noeud

    def supprimer(self, valeur):
        parent = None
        courant = self.racine
        while courant is not None and courant.valeur != valeur:
            parent = courant
            if valeur < courant.valeur:
                courant = courant.gauche
            else:
                courant = courant.droite
        if courant is not None:
            if courant.gauche is None and courant.droite is None:      #  nœud sans fils
                if parent is None:
                    self.racine = None
                elif parent.gauche == courant:
                    parent.gauche = None
                else:
                    parent.droite = None
            elif courant.gauche is None or courant.droite is None :
                enfant = courant.gauche if courant.gauche is not None else courant.droite
                if parent is None:
                    self.racine = enfant
                elif parent.gauche == courant:
                    parent.gauche = enfant
                else:
                    parent.droite = enfant
            else:							# noeud avec 2 fils
                successeur_parent = courant
                successeur = courant.droite
                while successeur.gauche is not None:
                    successeur_parent = successeur
                    successeur = successeur.gauche
                courant.valeur = successeur.valeur
                if successeur_parent.gauche == successeur:
                    successeur_parent.gauche = successeur.droite
                else:
                    successeur_parent.droite = successeur.droite
        return

    def afficher_en_ordre(self):
        self._afficher_en_ordre(self.racine)
        print()

    def _afficher_en_ordre(self, noeud):
        if noeud is not None:
            self._afficher_en_ordre(noeud.gauche)
            print(noeud.valeur, end=' ')
            self._afficher_en_ordre(noeud.droite)
