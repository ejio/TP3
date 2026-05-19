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
                parent.gauche = nouveau_noeud # type: ignore
            else:
                parent.droite = nouveau_noeud # type: ignore

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

class Categorie:
    def __init__(self, nom):
        self.nom = nom
        self.inventions = {}

    def __lt__(self, autre):
        return self.nom < autre.nom

    def __gt__(self, autre):
        return self.nom > autre.nom

    def __eq__(self, autre):
        return self.nom == autre.nom
    
class Invention:
    def __init__(self, nom, inventeur, annee):
        self.nom = nom
        self.inventeur = inventeur
        self.annee = annee
    def __str__(self):
        return self.nom

categories = ArbreBinaire()

def ajouter_categorie(nom):
    if categories.contient(nom) == 0:
        categories.ajouter(Categorie(nom))
    else:
        print(f"Il y a déjà une catégorie {nom}")

def rechercher_invention(noeud, invention):
    if noeud is None:
        return False, None

    if invention in noeud.valeur.inventions:
        return True, noeud.valeur.inventions[invention]

    resultat = rechercher_invention(noeud.gauche, invention)

    if resultat[0]:
        return resultat

    return rechercher_invention(noeud.droite, invention)

def ajouter_invention(categorie, nom, inventeur, annee):
    trouve, _ = rechercher_invention(categories.racine,nom)
    if not trouve:
        categorie.inventions[nom] = Invention(nom, inventeur, annee)
    else:
        print("Invention déjà ajoutée")

def modifier_annee(nom_invention, nouvelle_annee):
    trouve, invention = rechercher_invention(categories.racine, nom_invention)
    if trouve:
        invention.annee = nouvelle_annee # type: ignore
    else:
        print("Cette invention n'existe pas encore")

def afficher_invention_inventeur(inventeur, noeud=None):
    if noeud is None:
        noeud = categories.racine

    if noeud is None:
        return

    afficher_invention_inventeur(inventeur, noeud.gauche)

    for invention in noeud.valeur.inventions.values():
        if invention.inventeur == inventeur:
            print(invention.nom)

    afficher_invention_inventeur(inventeur, noeud.droite)
