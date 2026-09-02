# -*- coding: utf-8 -*-
"""
Tests automatiques pour blockblast.py

Ces tests ne lancent PAS le jeu : ils appellent directement les fonctions
et verifient qu'elles repondent ce qu'on attend.

  python tests_blockblast.py                    -> teste blockblast.py
  python tests_blockblast.py blockblast_corrige -> teste un autre fichier

Chaque test qui echoue t'indique la fonction a aller regarder.
Attention : les tests ne voient pas tout ! Deux bugs ne se remarquent
qu'en jouant vraiment a la partie.
"""

import sys
import importlib
import traceback

nom_module = sys.argv[1] if len(sys.argv) > 1 else "blockblast"
jeu = importlib.import_module(nom_module)

resultats = []


def verifier(titre, fonction, indice):
    """Lance un test et note s'il passe ou non."""
    try:
        fonction()
        resultats.append((True, titre, ""))
    except AssertionError as erreur:
        resultats.append((False, titre, str(erreur) + "\n     -> " + indice))
    except Exception:
        detail = traceback.format_exc().strip().splitlines()[-1]
        resultats.append((False, titre,
                          "le programme a plante : " + detail
                          + "\n     -> " + indice))


def grille_vide():
    """Une vraie grille vide, construite ici pour ne pas dependre du jeu."""
    return [[None for _ in range(jeu.GRID)] for _ in range(jeu.GRID)]


def piece(cases, couleur="#ff0000"):
    return {"cases": cases, "couleur": couleur}


# --------------------------------------------------------------- les tests
def test_grille_neuve():
    g = jeu.nouvelle_grille()
    assert len(g) == jeu.GRID, "la grille n'a pas 8 lignes"
    assert len(g[0]) == jeu.GRID, "une ligne n'a pas 8 colonnes"
    g[0][3] = "rouge"
    assert g[1][3] is None, ("j'ai ecrit UNE case (ligne 0, colonne 3) "
                             "et la case (ligne 1, colonne 3) a change aussi")


def test_peut_placer_dans_le_vide():
    g = grille_vide()
    assert jeu.peut_placer(g, piece([(0, 0), (0, 1)]), 0, 0) is True, \
        "une piece devrait rentrer dans une grille vide"


def test_peut_placer_refuse_a_droite():
    g = grille_vide()
    p = piece([(0, 0), (0, 1)])          # piece large de 2 cases
    resultat = jeu.peut_placer(g, p, 0, 7)   # colonnes 7 et 8 -> impossible
    assert resultat is False, ("la piece depasse a droite de la grille, "
                               "elle ne devrait pas etre acceptee")


def test_peut_placer_refuse_case_occupee():
    g = grille_vide()
    g[2][3] = "bleu"
    assert jeu.peut_placer(g, piece([(0, 0)]), 2, 3) is False, \
        "on ne devrait pas pouvoir poser une piece sur une case deja prise"


def test_placer_au_bon_endroit():
    g = grille_vide()
    jeu.placer(g, piece([(0, 0), (0, 1)], "vert"), 2, 0)
    assert g[2][0] == "vert" and g[2][1] == "vert", \
        ("la piece devait remplir la ligne 2, colonnes 0 et 1 ; "
         "cases remplies : " + str([(l, c) for l in range(jeu.GRID)
                                    for c in range(jeu.GRID)
                                    if g[l][c] is not None]))


def test_colonne_incomplete():
    g = grille_vide()
    g[0][4] = "jaune"                    # une seule case de la colonne 4
    lignes, colonnes = jeu.lignes_completes(g)
    assert colonnes == [], ("la colonne 4 n'a qu'une case remplie sur 8, "
                            "elle ne devrait pas etre consideree comme pleine")


def test_ligne_et_colonne_pleines():
    g = grille_vide()
    for c in range(jeu.GRID):
        g[5][c] = "rouge"                # ligne 5 pleine
    for l in range(jeu.GRID):
        g[l][2] = "rouge"                # colonne 2 pleine
    lignes, colonnes = jeu.lignes_completes(g)
    assert lignes == [5], "la ligne 5 est pleine, elle devrait etre detectee"
    assert colonnes == [2], "la colonne 2 est pleine, elle devrait etre detectee"


def test_effacer():
    g = grille_vide()
    for c in range(jeu.GRID):
        g[5][c] = "rouge"
    g[6][6] = "bleu"
    jeu.effacer(g, [5], [])
    assert all(g[5][c] is None for c in range(jeu.GRID)), \
        "la ligne 5 devait etre entierement videe"
    assert g[6][6] == "bleu", "seule la ligne 5 devait etre videe"


def test_case_visee():
    p = piece([(0, 0)])
    # souris pile au centre de la case (ligne 0, colonne 0)
    x = jeu.MARGE + jeu.CELL / 2
    y = jeu.HAUT + jeu.CELL / 2
    assert jeu.case_visee(p, x, y) == (0, 0), \
        "souris au centre de la case (0, 0), la piece devrait viser (0, 0)"
    # souris pile au centre de la case (ligne 3, colonne 5)
    x = jeu.MARGE + 5 * jeu.CELL + jeu.CELL / 2
    y = jeu.HAUT + 3 * jeu.CELL + jeu.CELL / 2
    assert jeu.case_visee(p, x, y) == (3, 5), \
        "souris au centre de la case (3, 5), la piece devrait viser (3, 5)"


def test_partie_pas_finie():
    g = grille_vide()
    pieces = [piece([(0, 0)]), piece([(0, 0), (0, 1)]), piece([(0, 0)])]
    assert jeu.partie_finie(g, pieces) is False, \
        "la grille est vide, la partie ne peut pas etre finie"


def test_partie_finie_seulement_si_rien_ne_rentre():
    g = grille_vide()
    for l in range(jeu.GRID):
        for c in range(jeu.GRID):
            g[l][c] = "gris"
    g[0][0] = None                       # une seule case libre
    petite = piece([(0, 0)])             # celle-la rentre
    grande = piece([(0, 0), (0, 1)])     # celle-la ne rentre pas
    assert jeu.partie_finie(g, [petite, grande]) is False, \
        ("une des deux pieces rentre encore : la partie n'est pas finie "
         "tant qu'il reste UN coup possible")
    assert jeu.partie_finie(g, [grande, grande]) is True, \
        "aucune des pieces ne rentre : la partie devrait etre finie"


# ------------------------------------------------------------- lancement
TESTS = [
    (test_grille_neuve,
     "nouvelle_grille : les 8 lignes sont-elles vraiment 8 listes differentes ?"),
    (test_peut_placer_dans_le_vide,
     "peut_placer : relis la boucle et les conditions"),
    (test_peut_placer_refuse_a_droite,
     "peut_placer : les 4 bords de la grille sont-ils tous testes ?"),
    (test_peut_placer_refuse_case_occupee,
     "peut_placer : le test de la case deja occupee"),
    (test_placer_au_bon_endroit,
     "placer : dans grille[a][b], qui est la ligne et qui est la colonne ?"),
    (test_colonne_incomplete,
     "lignes_completes : regarde l'indentation de la boucle des colonnes"),
    (test_ligne_et_colonne_pleines,
     "lignes_completes : la detection des colonnes"),
    (test_effacer,
     "effacer : les deux boucles"),
    (test_case_visee,
     "case_visee : la grille commence-t-elle en haut a gauche de la fenetre ?"),
    (test_partie_pas_finie,
     "partie_finie : relis la condition"),
    (test_partie_finie_seulement_si_rien_ne_rentre,
     "partie_finie : 'au moins une' ou 'toutes' ? (any / all)"),
]

print("")
print("Tests de " + nom_module + ".py")
print("=" * 60)

for fonction, indice in TESTS:
    verifier(fonction.__name__, fonction, indice)

reussis = 0
for ok, titre, message in resultats:
    if ok:
        print("[ OK ] " + titre)
        reussis += 1
    else:
        print("[FAIL] " + titre)
        for ligne in message.splitlines():
            print("       " + ligne)

print("=" * 60)
print(str(reussis) + " / " + str(len(resultats)) + " tests reussis")
if reussis < len(resultats):
    print("")
    print("Repare le PREMIER test qui echoue, relance, recommence.")
else:
    print("")
    print("Tous les tests passent. Lance le jeu et verifie qu'il se joue bien :")
    print("il reste 2 bugs que les tests ne peuvent pas voir.")
