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

def rechercher_categorie(noeud, categorie):
    if noeud is None:
        return None
    if noeud.valeur.nom == categorie:
        return noeud
    if categorie < noeud.valeur.nom:
        return rechercher_categorie(noeud.gauche, categorie)
    return rechercher_categorie(noeud.droite, categorie)

def ajouter_categorie(nom):
    noeud = rechercher_categorie(categories.racine, nom)
    if noeud is None:
        categories.ajouter(Categorie(nom))
        print(f"Ajout catégorie {nom}")
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
    noeud_categorie = rechercher_categorie(categories.racine, categorie)
    if noeud_categorie is None:
        print(f"Il n'y a pas de catégorie {categorie}")
        return
    trouve, _ = rechercher_invention(categories.racine, nom)
    if trouve:
        print(f"L'invention {nom} existe déjà")
        return
    noeud_categorie.valeur.inventions[nom] = Invention(nom, inventeur, annee)
    print(f"Ajout de l'invention {nom}, à la catégorie {categorie}")

def modifier_annee(nom_invention, nouvelle_annee):
    trouve, invention = rechercher_invention(categories.racine, nom_invention)
    if trouve:
        invention.annee = nouvelle_annee # type: ignore
        print(f"Modification de l'année de {nom_invention} par {nouvelle_annee}")
    else:
        print("Cette invention n'existe pas encore")

def afficher_invention_inventeur(inventeur, noeud=None, _premier_appel=True):
    if _premier_appel:
        noeud = categories.racine
        print(f"Inventions de {inventeur}")
    if noeud is None:
        return
    afficher_invention_inventeur(inventeur, noeud.gauche, _premier_appel=False)
    for invention in noeud.valeur.inventions.values():
        if invention.inventeur == inventeur:
            print(invention.nom, "inventée en", invention.annee)
    afficher_invention_inventeur(inventeur, noeud.droite, _premier_appel=False)

def afficher_categorie_inventions(noeud=None, _premier_appel=True):
    if _premier_appel:
        noeud = categories.racine
        print("Catégories et inventions :")
    if noeud is None:
        return
    afficher_categorie_inventions(noeud.gauche, _premier_appel=False)
    categorie = noeud.valeur
    print(categorie.nom)
    if categorie.inventions:
        for invention in categorie.inventions.values():
            print(f"    - {invention.nom} | {invention.inventeur} | {invention.annee}")
    else:
        print("aucune invention")
    afficher_categorie_inventions(noeud.droite, _premier_appel=False)

ajouter_categorie("math")
ajouter_invention("math", "derive", "Newton", 1500)
afficher_invention_inventeur("Newton")