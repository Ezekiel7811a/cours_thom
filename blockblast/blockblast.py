# -*- coding: utf-8 -*-
"""
BLOCK BLAST - version a deboguer.

Le jeu :
  - une grille de 8 x 8 cases
  - 3 pieces en bas de l'ecran, a poser dans la grille avec la souris
  - quand une ligne OU une colonne est pleine, elle explose et rapporte des points
  - quand les 3 pieces sont posees, 3 nouvelles arrivent
  - la partie est finie quand plus aucune piece ne rentre

ATTENTION : ce programme contient 8 bugs volontaires.
Aucun commentaire ne t'indique ou ils sont : a toi de les trouver !

Lancer le jeu :        python blockblast.py
Lancer les tests :     python tests_blockblast.py
"""

import random
import tkinter as tk

# --------------------------------------------------------------- constantes
GRID = 8            # la grille fait 8 cases sur 8
CELL = 50           # taille d'une case de la grille, en pixels
MARGE = 40          # espace a gauche avant la grille
HAUT = 90           # espace en haut avant la grille
TRAY_CELL = 26      # taille d'une case des pieces en reserve
TRAY_Y = 530        # hauteur ou commence la reserve de pieces
LARGEUR = MARGE * 2 + GRID * CELL
HAUTEUR = 680

FOND = "#181a26"
CASE_VIDE = "#2c3042"
TEXTE = "#ebebf5"
GRIS = "#6b7089"

COULEURS = ["#ef5350", "#ffa726", "#ffee58", "#66bb6a",
            "#42a5f5", "#ab47bc", "#26c6da"]

# Une forme = la liste des cases qu'elle occupe, en (ligne, colonne)
FORMES = [
    [(0, 0)],
    [(0, 0), (0, 1)],
    [(0, 0), (1, 0)],
    [(0, 0), (0, 1), (0, 2)],
    [(0, 0), (1, 0), (2, 0)],
    [(0, 0), (0, 1), (0, 2), (0, 3)],
    [(0, 0), (1, 0), (2, 0), (3, 0)],
    [(0, 0), (0, 1), (1, 0), (1, 1)],
    [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2)],
    [(0, 0), (0, 1), (1, 0), (1, 1), (2, 0), (2, 1)],
    [(0, 0), (1, 0), (1, 1)],
    [(0, 0), (0, 1), (1, 0)],
    [(0, 0), (0, 1), (1, 1)],
    [(0, 1), (1, 0), (1, 1)],
    [(0, 0), (1, 0), (2, 0), (2, 1)],
    [(0, 1), (1, 1), (2, 0), (2, 1)],
    [(0, 0), (0, 1), (0, 2), (1, 1)],
    [(0, 1), (0, 2), (1, 0), (1, 1)],
]


# ---------------------------------------------------------------- la grille
def nouvelle_grille():
    """Renvoie une grille 8x8 vide (None = case vide)."""
    return [[None] * GRID] * GRID


def nouvelle_piece():
    """Tire au hasard une nouvelle piece."""
    return {"cases": random.choice(FORMES), "couleur": random.choice(COULEURS)}


def taille_piece(piece):
    """Renvoie (nb_lignes, nb_colonnes) occupees par la piece."""
    hauteur = max(l for l, c in piece["cases"]) + 1
    largeur = max(c for l, c in piece["cases"]) + 1
    return hauteur, largeur


def peut_placer(grille, piece, lig, col):
    """Dit si la piece rentre dans la grille a partir de la case (lig, col)."""
    for dl, dc in piece["cases"]:
        l = lig + dl
        c = col + dc
        if l < 0 or c < 0 or l >= GRID:
            return False
        if grille[l][c] is not None:
            return False
    return True


def placer(grille, piece, lig, col):
    """Pose la piece dans la grille a partir de la case (lig, col)."""
    for dl, dc in piece["cases"]:
        grille[col + dc][lig + dl] = piece["couleur"]


def lignes_completes(grille):
    """Renvoie (liste des lignes pleines, liste des colonnes pleines)."""
    lignes = []
    colonnes = []

    for l in range(GRID):
        plein = True
        for c in range(GRID):
            if grille[l][c] is None:
                plein = False
        if plein:
            lignes.append(l)

    for c in range(GRID):
        plein = True
        for l in range(GRID):
            if grille[l][c] is None:
                plein = False
            break
        if plein:
            colonnes.append(c)

    return lignes, colonnes


def effacer(grille, lignes, colonnes):
    """Vide les lignes et les colonnes indiquees."""
    for l in lignes:
        for c in range(GRID):
            grille[l][c] = None
    for c in colonnes:
        for l in range(GRID):
            grille[l][c] = None


def piece_placable(grille, piece):
    """Dit s'il existe au moins un endroit ou poser cette piece."""
    for l in range(GRID):
        for c in range(GRID):
            if peut_placer(grille, piece, l, c):
                return True
    return False


def partie_finie(grille, pieces):
    """La partie est finie quand AUCUNE piece restante ne peut etre posee."""
    restantes = [p for p in pieces if p is not None]
    if len(restantes) == 0:
        return False
    return any(not piece_placable(grille, p) for p in restantes)


def case_visee(piece, x, y):
    """Convertit la position de la souris (x, y) en case (ligne, colonne)."""
    hauteur, largeur = taille_piece(piece)
    coin_x = x - largeur * CELL / 2
    coin_y = y - hauteur * CELL / 2
    col = round(coin_x / CELL)
    lig = round(coin_y / CELL)
    return lig, col


# --------------------------------------------------------- etat de la partie
grille = nouvelle_grille()
pieces = [nouvelle_piece(), nouvelle_piece(), nouvelle_piece()]
score = 0
fini = False
drag = None          # piece actuellement tenue par la souris
canvas = None


def nouvelle_partie():
    global grille, pieces, score, fini, drag
    grille = nouvelle_grille()
    pieces = [nouvelle_piece(), nouvelle_piece(), nouvelle_piece()]
    score = 0
    fini = False
    drag = None
    dessiner()


# -------------------------------------------------------------- l'affichage
def case(x, y, taille, couleur):
    canvas.create_rectangle(x + 2, y + 2, x + taille - 2, y + taille - 2,
                            fill=couleur, outline="", width=0)


def dessiner_piece(piece, x, y, taille):
    for dl, dc in piece["cases"]:
        case(x + dc * taille, y + dl * taille, taille, piece["couleur"])


def slot_x(i):
    """Centre horizontal du i-eme emplacement de la reserve."""
    return 80 + i * 160


def dessiner():
    canvas.delete("all")

    canvas.create_text(LARGEUR / 2, 32, text="BLOCK BLAST",
                       fill=TEXTE, font=("Segoe UI", 24, "bold"))
    canvas.create_text(LARGEUR / 2, 63, text="Score : " + str(score),
                       fill=GRIS, font=("Segoe UI", 14))

    # la grille
    for l in range(GRID):
        for c in range(GRID - 1):
            couleur = grille[l][c]
            if couleur is None:
                couleur = CASE_VIDE
            case(MARGE + c * CELL, HAUT + l * CELL, CELL, couleur)

    # apercu de l'endroit ou la piece va tomber
    if drag is not None:
        piece = pieces[drag["i"]]
        lig, col = case_visee(piece, drag["x"], drag["y"])
        if peut_placer(grille, piece, lig, col):
            for dl, dc in piece["cases"]:
                x = MARGE + (col + dc) * CELL
                y = HAUT + (lig + dl) * CELL
                canvas.create_rectangle(x + 2, y + 2, x + CELL - 2,
                                        y + CELL - 2, fill=piece["couleur"],
                                        outline="", stipple="gray50")

    # la reserve de 3 pieces
    for i in range(3):
        piece = pieces[i]
        if piece is None:
            continue
        if drag is not None and drag["i"] == i:
            continue
        hauteur, largeur = taille_piece(piece)
        x = slot_x(i) - largeur * TRAY_CELL / 2
        y = TRAY_Y + 60 - hauteur * TRAY_CELL / 2
        dessiner_piece(piece, x, y, TRAY_CELL)

    # la piece tenue par la souris
    if drag is not None:
        piece = pieces[drag["i"]]
        hauteur, largeur = taille_piece(piece)
        x = drag["x"] - largeur * CELL / 2
        y = drag["y"] - hauteur * CELL / 2
        dessiner_piece(piece, x, y, CELL)

    if fini:
        canvas.create_rectangle(0, 230, LARGEUR, 350, fill=FOND, outline="")
        canvas.create_text(LARGEUR / 2, 270, text="PARTIE TERMINEE",
                           fill="#ef5350", font=("Segoe UI", 26, "bold"))
        canvas.create_text(LARGEUR / 2, 315, text="Appuie sur R pour rejouer",
                           fill=TEXTE, font=("Segoe UI", 14))


# ----------------------------------------------------------------- la souris
def slot_sous_souris(x, y):
    """Renvoie le numero de l'emplacement clique, ou None."""
    for i in range(3):
        if abs(x - slot_x(i)) < 70 and TRAY_Y <= y <= TRAY_Y + 120:
            return i
    return None


def souris_appuyee(event):
    global drag
    if fini:
        return
    i = slot_sous_souris(event.x, event.y)
    if i is not None and pieces[i] is not None:
        drag = {"i": i, "x": event.x, "y": event.y}
        dessiner()


def souris_bougee(event):
    if drag is None:
        return
    drag["x"] = event.x
    drag["y"] = event.y
    dessiner()


def souris_relachee(event):
    global drag, score, pieces, fini
    if drag is None:
        return

    i = drag["i"]
    piece = pieces[i]
    lig, col = case_visee(piece, event.x, event.y)

    if peut_placer(grille, piece, lig, col):
        placer(grille, piece, lig, col)
        points = len(piece["cases"])

        lignes, colonnes = lignes_completes(grille)
        effacer(grille, lignes, colonnes)
        nb = len(lignes) + len(colonnes)
        points = points + 10 * nb * nb

        score = points
        pieces[i] = None

        if pieces[0] is None and pieces[1] is None and pieces[2] is None:
            pieces = [nouvelle_piece(), nouvelle_piece(), nouvelle_piece()]

        fini = partie_finie(grille, pieces)

    drag = None
    dessiner()


def touche(event):
    if event.char.lower() == "r":
        nouvelle_partie()


# -------------------------------------------------------------------- depart
def main():
    global canvas
    fenetre = tk.Tk()
    fenetre.title("Block Blast")
    fenetre.resizable(False, False)
    canvas = tk.Canvas(fenetre, width=LARGEUR, height=HAUTEUR,
                       bg=FOND, highlightthickness=0)
    canvas.pack()
    canvas.bind("<Button-1>", souris_appuyee)
    canvas.bind("<B1-Motion>", souris_bougee)
    canvas.bind("<ButtonRelease-1>", souris_relachee)
    fenetre.bind("<Key>", touche)
    dessiner()
    fenetre.mainloop()


if __name__ == "__main__":
    main()
