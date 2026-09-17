# -*- coding: utf-8 -*-
"""
DEMINEUR - code a trous.

Le jeu est presque fini : il manque des morceaux dans 10 fonctions,
numerotees de l'etape 1 a l'etape 10. Fais-les DANS L'ORDRE.

  NIVEAU 1 (etapes 1 a 4)   remplace chaque ____ par une expression.
  NIVEAU 2 (etapes 5 a 7)   des lignes entieres ont disparu.
  NIVEAU 3 (etapes 8 a 10)  il ne reste que le nom et la description :
                            ecris toute la fonction.

Apres chaque etape, lance les tests :

    python tests_demineur.py

Quand les 10 etapes passent, lance le jeu :

    python demineur.py

Tout ce qui est apres l'etape 10 marche deja : tu n'as rien a y toucher
(mais tu as le droit de le lire).
"""

import random
import tkinter as tk

# --------------------------------------------------------------- constantes
LIGNES = 9          # nombre de lignes de la grille
COLONNES = 12       # nombre de colonnes
MINES = 15          # nombre de mines cachees
CELL = 40           # taille d'une case, en pixels
MARGE = 20          # espace a gauche (et a droite, et en bas) de la grille
HAUT = 70           # espace en haut, pour le compteur
LARGEUR = MARGE * 2 + COLONNES * CELL
HAUTEUR = HAUT + LIGNES * CELL + MARGE

FOND = "#181a26"
FERMEE = "#4a5070"
FERMEE_CLAIR = "#5c6386"
OUVERTE = "#d9dbe6"
EXPLOSION = "#ef5350"
TEXTE = "#ebebf5"
GRIS = "#6b7089"

# couleur du chiffre selon le nombre de mines voisines
COULEURS_CHIFFRES = {1: "#1e63d6", 2: "#2e8b3a", 3: "#d32f2f", 4: "#1a237e",
                     5: "#8d2a1b", 6: "#00838f", 7: "#000000", 8: "#555555"}


# ================================================================= NIVEAU 1
#                                    remplace chaque ____ par ce qu'il faut
# ------------------------------------------------------------------ etape 1
def nouvelle_grille(valeur):
    """Renvoie une grille LIGNES x COLONNES dont toutes les cases valent
    `valeur`. Exemple : nouvelle_grille(False)."""
    return [[____ for _ in range(____)] for _ in range(____)]


# ------------------------------------------------------------------ etape 2
def dans_grille(lig, col):
    """True si la case (lig, col) existe dans la grille, False sinon."""
    return 0 <= lig < ____ and ____


# ------------------------------------------------------------------ etape 3
def voisins(lig, col):
    """Renvoie la liste des cases voisines de (lig, col), diagonales
    comprises, sans la case elle-meme et sans sortir de la grille."""
    liste = []
    for dl in (-1, 0, 1):
        for dc in (-1, 0, 1):
            if ____:
                continue
            l, c = ____, ____
            if dans_grille(l, c):
                liste.append((l, c))
    return liste


# ------------------------------------------------------------------ etape 4
def compter_mines(mines, lig, col):
    """Nombre de mines dans les cases voisines de (lig, col)."""
    n = 0
    for l, c in voisins(lig, col):
        if ____:
            n = ____
    return n


# ================================================================= NIVEAU 2
#                                     chaque ________ est une ligne entiere
# ------------------------------------------------------------------ etape 5
def poser_mines(nb, lig0, col0):
    """Cache `nb` mines au hasard. La case (lig0, col0), celle du premier
    clic, et ses voisines ne recoivent jamais de mine."""
    mines = nouvelle_grille(False)
    interdites = [(lig0, col0)] + voisins(lig0, col0)
    candidates = [(l, c) for l in range(LIGNES) for c in range(COLONNES)
                  if (l, c) not in interdites]
    # tirer nb cases au hasard parmi les candidates, et les ranger dans
    # une variable `choisies` (indice : cherche random.sample)
    ________________________________________________________________
    for l, c in choisies:
        mines[l][c] = True
    return mines


# ------------------------------------------------------------------ etape 6
def basculer_drapeau(ouvert, drapeaux, lig, col):
    """Pose un drapeau sur une case fermee, ou l'enleve s'il y en a deja un.
    On ne peut pas mettre de drapeau sur une case deja ouverte."""
    if ________________________:
        return
    ________________________________________________________________


# ------------------------------------------------------------------ etape 7
def reveler(mines, ouvert, drapeaux, lig, col):
    """Ouvre la case (lig, col). Si elle n'a aucune mine autour, ouvre aussi
    toutes ses voisines, qui ouvrent leurs voisines, etc."""
    if not dans_grille(lig, col):
        return
    if ________________________________________:
        return
    ouvert[lig][col] = True
    if mines[lig][col]:
        return
    if compter_mines(mines, lig, col) == 0:
        for l, c in ________________________:
            ________________________________________________________


# ================================================================= NIVEAU 3
#                                          ecris la fonction toute entiere
# ------------------------------------------------------------------ etape 8
def a_gagne(mines, ouvert):
    """True si toutes les cases SANS mine sont ouvertes."""
    # A COMPLETER (et supprime la ligne raise)
    raise NotImplementedError("etape 8")


# ------------------------------------------------------------------ etape 9
def case_cliquee(x, y):
    """Convertit la position (x, y) de la souris, en pixels, en (lig, col).
    Renvoie None si on a clique en dehors de la grille."""
    # A COMPLETER (et supprime la ligne raise)
    raise NotImplementedError("etape 9")


# ----------------------------------------------------------------- etape 10
def ouvrir_autour(mines, ouvert, drapeaux, lig, col):
    """Clic sur un chiffre deja ouvert : si le nombre de drapeaux autour est
    egal au chiffre, ouvre toutes les voisines qui n'ont pas de drapeau."""
    # A COMPLETER (et supprime la ligne raise)
    raise NotImplementedError("etape 10")


# ========================================= a partir d'ici, rien a completer
def mine_ouverte(mines, ouvert):
    """True si une mine a ete ouverte (partie perdue)."""
    for l in range(LIGNES):
        for c in range(COLONNES):
            if mines[l][c] and ouvert[l][c]:
                return True
    return False


# ------------------------------------------------------------ etat du jeu
mines = None        # None tant qu'on n'a pas fait le premier clic
ouvert = None
drapeaux = None
etat = "jeu"        # "jeu", "perdu" ou "gagne"
explosion = None    # la case de la mine qui a saute
canvas = None


def nouvelle_partie():
    global mines, ouvert, drapeaux, etat, explosion
    mines = None
    ouvert = nouvelle_grille(False)
    drapeaux = nouvelle_grille(False)
    etat = "jeu"
    explosion = None
    if canvas is not None:
        dessiner()


# ------------------------------------------------------------------ dessin
def dessiner_drapeau(x, y):
    canvas.create_line(x + 16, y + 10, x + 16, y + 31, fill="#222222", width=2)
    canvas.create_polygon(x + 17, y + 9, x + 29, y + 15, x + 17, y + 21,
                          fill=EXPLOSION, outline="")
    canvas.create_line(x + 11, y + 31, x + 23, y + 31, fill="#222222", width=2)


def dessiner_mine(x, y):
    m = CELL / 2
    for dx, dy in ((0, -11), (0, 11), (-11, 0), (11, 0)):
        canvas.create_line(x + m, y + m, x + m + dx, y + m + dy,
                           fill="#111111", width=2)
    canvas.create_oval(x + m - 8, y + m - 8, x + m + 8, y + m + 8,
                       fill="#111111", outline="")
    canvas.create_oval(x + m - 4, y + m - 5, x + m - 1, y + m - 2,
                       fill="#ffffff", outline="")


def dessiner():
    canvas.delete("all")

    nb_drapeaux = sum(ligne.count(True) for ligne in drapeaux)
    canvas.create_text(MARGE, HAUT / 2, anchor="w",
                       text="Mines : " + str(MINES - nb_drapeaux),
                       fill=TEXTE, font=("Segoe UI", 16, "bold"))
    if etat == "perdu":
        message, couleur = "PERDU  (R pour rejouer)", EXPLOSION
    elif etat == "gagne":
        message, couleur = "GAGNE !  (R pour rejouer)", "#66bb6a"
    else:
        message, couleur = "clic droit = drapeau", GRIS
    canvas.create_text(LARGEUR - MARGE, HAUT / 2, anchor="e", text=message,
                       fill=couleur, font=("Segoe UI", 12, "bold"))

    for l in range(LIGNES):
        for c in range(COLONNES):
            x = MARGE + c * CELL
            y = HAUT + l * CELL
            fin = etat != "jeu"
            est_mine = mines is not None and mines[l][c]

            if ouvert[l][c] or (fin and est_mine and not drapeaux[l][c]):
                fond = EXPLOSION if (l, c) == explosion else OUVERTE
                canvas.create_rectangle(x, y, x + CELL, y + CELL,
                                        fill=fond, outline="#aeb1c2")
                if est_mine:
                    dessiner_mine(x, y)
                else:
                    n = compter_mines(mines, l, c)
                    if n > 0:
                        canvas.create_text(x + CELL / 2, y + CELL / 2,
                                           text=str(n),
                                           fill=COULEURS_CHIFFRES[n],
                                           font=("Segoe UI", 16, "bold"))
            else:
                canvas.create_rectangle(x, y, x + CELL, y + CELL,
                                        fill=FERMEE, outline=FOND)
                canvas.create_rectangle(x + 3, y + 3, x + CELL - 3,
                                        y + CELL - 3, fill=FERMEE_CLAIR,
                                        outline="")
                if drapeaux[l][c]:
                    dessiner_drapeau(x, y)
                    if fin and not est_mine:
                        # drapeau pose au mauvais endroit
                        canvas.create_line(x + 6, y + 6, x + CELL - 6,
                                           y + CELL - 6, fill="#111111",
                                           width=3)
                        canvas.create_line(x + CELL - 6, y + 6, x + 6,
                                           y + CELL - 6, fill="#111111",
                                           width=3)


# ----------------------------------------------------------------- la souris
def clic_gauche(event):
    global mines, etat, explosion
    if etat != "jeu":
        return
    case = case_cliquee(event.x, event.y)
    if case is None:
        return
    lig, col = case
    if drapeaux[lig][col]:
        return

    if mines is None:
        mines = poser_mines(MINES, lig, col)

    if ouvert[lig][col]:
        ouvrir_autour(mines, ouvert, drapeaux, lig, col)
    else:
        reveler(mines, ouvert, drapeaux, lig, col)

    if mine_ouverte(mines, ouvert):
        etat = "perdu"
        for l in range(LIGNES):
            for c in range(COLONNES):
                if mines[l][c] and ouvert[l][c]:
                    explosion = (l, c)
    elif a_gagne(mines, ouvert):
        etat = "gagne"
    dessiner()


def clic_droit(event):
    if etat != "jeu":
        return
    case = case_cliquee(event.x, event.y)
    if case is None:
        return
    lig, col = case
    basculer_drapeau(ouvert, drapeaux, lig, col)
    dessiner()


def touche(event):
    if event.char.lower() == "r":
        nouvelle_partie()


# -------------------------------------------------------------------- depart
def main():
    global canvas
    fenetre = tk.Tk()
    fenetre.title("Demineur")
    fenetre.resizable(False, False)
    canvas = tk.Canvas(fenetre, width=LARGEUR, height=HAUTEUR,
                       bg=FOND, highlightthickness=0)
    canvas.pack()
    canvas.bind("<Button-1>", clic_gauche)
    canvas.bind("<Button-3>", clic_droit)     # clic droit (Windows, Linux)
    canvas.bind("<Button-2>", clic_droit)     # clic droit (Mac)
    fenetre.bind("<Key>", touche)
    nouvelle_partie()
    fenetre.mainloop()


if __name__ == "__main__":
    main()
