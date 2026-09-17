# -*- coding: utf-8 -*-
"""
Tests automatiques pour demineur.py

Ces tests ne lancent PAS le jeu : ils appellent directement les fonctions
et verifient qu'elles repondent ce qu'on attend.

  python tests_demineur.py                  -> teste demineur.py
  python tests_demineur.py demineur_corrige -> teste un autre fichier

Les tests sont ranges par etape, dans le meme ordre que le fichier.
Travaille toujours sur la PREMIERE etape qui n'est pas validee.
"""

import os
import sys
import importlib
import traceback

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
nom_module = sys.argv[1] if len(sys.argv) > 1 else "demineur"
jeu = importlib.import_module(nom_module)


# ------------------------------------------------------------- outils
def grille(valeur):
    """Une vraie grille, construite ici pour ne pas dependre du jeu."""
    return [[valeur for _ in range(jeu.COLONNES)] for _ in range(jeu.LIGNES)]


def mines_en(*cases):
    """Une grille de mines avec des mines exactement sur ces cases."""
    m = grille(False)
    for l, c in cases:
        m[l][c] = True
    return m


def cases_vraies(g):
    return [(l, c) for l in range(jeu.LIGNES) for c in range(jeu.COLONNES)
            if g[l][c]]


def nb_vraies(g):
    return len(cases_vraies(g))


# --------------------------------------------------------- etape 1
def test_grille_dimensions():
    g = jeu.nouvelle_grille("x")
    assert len(g) == jeu.LIGNES, \
        "la grille devrait avoir %d lignes, elle en a %d" % (jeu.LIGNES, len(g))
    assert len(g[0]) == jeu.COLONNES, \
        "une ligne devrait avoir %d cases, elle en a %d" % (jeu.COLONNES,
                                                             len(g[0]))
    assert all(v == "x" for ligne in g for v in ligne), \
        "nouvelle_grille(\"x\") : toutes les cases devraient valoir \"x\""


def test_grille_lignes_independantes():
    g = jeu.nouvelle_grille(False)
    g[0][3] = True
    assert g[1][3] is False, \
        ("j'ai change UNE case (ligne 0, colonne 3) et la case "
         "(ligne 1, colonne 3) a change aussi")


# --------------------------------------------------------- etape 2
def test_dans_grille():
    L, C = jeu.LIGNES, jeu.COLONNES
    attendus = [((0, 0), True), ((L - 1, C - 1), True), ((4, 2), True),
                ((-1, 0), False), ((0, -1), False),
                ((L, 0), False), ((0, C), False), ((L, C), False),
                ((0, L), True), ((C - 1, 0), False)]
    for (l, c), attendu in attendus:
        obtenu = jeu.dans_grille(l, c)
        assert obtenu == attendu, \
            "dans_grille(%d, %d) devrait donner %s, pas %s" % (l, c, attendu,
                                                               obtenu)


# --------------------------------------------------------- etape 3
def test_voisins_au_milieu():
    v = jeu.voisins(4, 4)
    attendu = {(3, 3), (3, 4), (3, 5), (4, 3), (4, 5), (5, 3), (5, 4), (5, 5)}
    assert (4, 4) not in v, "la case (4, 4) n'est pas sa propre voisine"
    assert set(v) == attendu and len(v) == 8, \
        "voisins(4, 4) devrait donner les 8 cases autour, j'ai : " + str(v)


def test_voisins_dans_un_coin():
    v = jeu.voisins(0, 0)
    assert set(v) == {(0, 1), (1, 0), (1, 1)} and len(v) == 3, \
        "voisins(0, 0) : une case de coin a 3 voisines, j'ai : " + str(v)
    L, C = jeu.LIGNES, jeu.COLONNES
    v = jeu.voisins(L - 1, C - 1)
    assert len(v) == 3, \
        "voisins(%d, %d) : le coin en bas a droite a 3 voisines, j'ai : %s" \
        % (L - 1, C - 1, v)


# --------------------------------------------------------- etape 4
def test_compter_mines():
    m = mines_en((0, 0), (0, 1), (2, 2))
    n = jeu.compter_mines(m, 1, 1)
    assert n == 3, "3 mines autour de (1, 1), compter_mines donne %s" % n
    n = jeu.compter_mines(m, 0, 0)
    assert n == 1, ("(0, 0) est une mine mais ne compte pas pour elle-meme : "
                    "une seule mine voisine, compter_mines donne %s" % n)
    L, C = jeu.LIGNES, jeu.COLONNES
    n = jeu.compter_mines(m, L - 1, C - 1)
    assert n == 0, "aucune mine autour de (%d, %d), compter_mines donne %s" \
        % (L - 1, C - 1, n)


# --------------------------------------------------------- etape 5
def test_poser_mines_nombre_et_zone():
    for _ in range(30):
        m = jeu.poser_mines(10, 4, 4)
        assert len(m) == jeu.LIGNES and len(m[0]) == jeu.COLONNES, \
            "poser_mines doit renvoyer une grille complete"
        assert nb_vraies(m) == 10, \
            "j'ai demande 10 mines, il y en a %d" % nb_vraies(m)
        interdites = [(4, 4)] + [(4 + dl, 4 + dc) for dl in (-1, 0, 1)
                                 for dc in (-1, 0, 1)]
        for l, c in interdites:
            assert not m[l][c], \
                ("premier clic en (4, 4) : il y a une mine en (%d, %d), "
                 "on perdrait des le premier clic" % (l, c))


def test_poser_mines_au_hasard():
    parties = [cases_vraies(jeu.poser_mines(10, 0, 0)) for _ in range(10)]
    assert any(p != parties[0] for p in parties), \
        "10 parties de suite avec les mines exactement aux memes endroits"


# --------------------------------------------------------- etape 6
def test_drapeau_pose_et_enleve():
    ouvert, drapeaux = grille(False), grille(False)
    jeu.basculer_drapeau(ouvert, drapeaux, 2, 5)
    assert drapeaux[2][5] is True, "le premier clic droit doit poser le drapeau"
    assert nb_vraies(drapeaux) == 1, "un seul drapeau devait etre pose"
    jeu.basculer_drapeau(ouvert, drapeaux, 2, 5)
    assert drapeaux[2][5] is False, "le deuxieme clic droit doit l'enlever"


def test_pas_de_drapeau_sur_case_ouverte():
    ouvert, drapeaux = grille(False), grille(False)
    ouvert[3][3] = True
    jeu.basculer_drapeau(ouvert, drapeaux, 3, 3)
    assert drapeaux[3][3] is False, \
        "la case (3, 3) est deja ouverte : pas de drapeau dessus"


# --------------------------------------------------------- etape 7
def test_reveler_un_chiffre():
    m = mines_en((0, 0))
    ouvert = grille(False)
    jeu.reveler(m, ouvert, grille(False), 1, 1)
    assert cases_vraies(ouvert) == [(1, 1)], \
        ("(1, 1) touche une mine : on ouvre juste cette case. "
         "Cases ouvertes : " + str(cases_vraies(ouvert)))


def test_reveler_en_cascade():
    m = mines_en((0, 0))
    ouvert = grille(False)
    jeu.reveler(m, ouvert, grille(False), jeu.LIGNES - 1, jeu.COLONNES - 1)
    total = jeu.LIGNES * jeu.COLONNES
    assert not ouvert[0][0], "la mine (0, 0) n'aurait pas du etre ouverte"
    assert nb_vraies(ouvert) == total - 1, \
        ("une seule mine en (0, 0) et clic dans le coin oppose : toutes les autres "
         "cases (%d) devraient s'ouvrir en cascade, il y en a %d"
         % (total - 1, nb_vraies(ouvert)))


def test_reveler_respecte_les_drapeaux():
    m = mines_en((0, 0))
    ouvert, drapeaux = grille(False), grille(False)
    drapeaux[4][4] = True
    jeu.reveler(m, ouvert, drapeaux, 4, 4)
    assert nb_vraies(ouvert) == 0, \
        "on ne doit pas ouvrir une case qui porte un drapeau"
    jeu.reveler(m, ouvert, drapeaux, jeu.LIGNES - 1, jeu.COLONNES - 1)
    assert not ouvert[4][4], \
        "la cascade ne doit pas ouvrir la case (4, 4), qui porte un drapeau"


def test_reveler_une_mine():
    m = mines_en((0, 0))
    ouvert = grille(False)
    jeu.reveler(m, ouvert, grille(False), 0, 0)
    assert cases_vraies(ouvert) == [(0, 0)], \
        ("on clique sur la mine (0, 0) : elle s'ouvre (on a perdu) mais "
         "rien d'autre. Cases ouvertes : %d" % nb_vraies(ouvert))


# --------------------------------------------------------- etape 8
def test_a_gagne():
    m = mines_en((0, 0), (5, 5))
    ouvert = grille(True)
    ouvert[0][0] = ouvert[5][5] = False
    assert jeu.a_gagne(m, ouvert) is True, \
        "toutes les cases sans mine sont ouvertes : c'est gagne"
    assert jeu.a_gagne(m, grille(False)) is False, \
        "rien n'est ouvert : ce n'est pas gagne"


def test_a_gagne_regarde_toute_la_grille():
    m = mines_en((0, 0))
    for l, c in [(0, 1), (4, 4), (jeu.LIGNES - 1, jeu.COLONNES - 1)]:
        ouvert = grille(True)
        ouvert[0][0] = False
        ouvert[l][c] = False
        assert jeu.a_gagne(m, ouvert) is False, \
            ("la case (%d, %d) n'a pas de mine et n'est pas ouverte : "
             "ce n'est pas encore gagne" % (l, c))


# --------------------------------------------------------- etape 9
def centre(l, c):
    return (jeu.MARGE + c * jeu.CELL + jeu.CELL // 2,
            jeu.HAUT + l * jeu.CELL + jeu.CELL // 2)


def test_case_cliquee_dans_la_grille():
    for l, c in [(0, 0), (3, 5), (jeu.LIGNES - 1, jeu.COLONNES - 1)]:
        x, y = centre(l, c)
        obtenu = jeu.case_cliquee(x, y)
        assert obtenu == (l, c), \
            ("clic au centre de la case (lig=%d, col=%d), pixel (x=%d, y=%d) :"
             " j'obtiens %s" % (l, c, x, y, obtenu))
        assert all(type(v) is int for v in obtenu), \
            "lig et col doivent etre des entiers (int), pas %s" % (obtenu,)


def test_case_cliquee_bords():
    droite = jeu.MARGE + jeu.COLONNES * jeu.CELL
    bas = jeu.HAUT + jeu.LIGNES * jeu.CELL
    cas = [((droite - 1, bas - 1), (jeu.LIGNES - 1, jeu.COLONNES - 1),
            "le tout dernier pixel de la grille"),
           ((droite, 100), None, "juste a droite de la grille"),
           ((100, bas), None, "juste en dessous de la grille"),
           ((jeu.MARGE - 5, 100), None, "5 pixels a gauche de la grille"),
           ((100, jeu.HAUT - 5), None, "5 pixels au-dessus de la grille")]
    for (x, y), attendu, ou in cas:
        obtenu = jeu.case_cliquee(x, y)
        assert obtenu == attendu, \
            "clic %s (x=%d, y=%d) : attendu %s, obtenu %s" % (ou, x, y,
                                                             attendu, obtenu)


# -------------------------------------------------------- etape 10
def test_ouvrir_autour_sans_drapeau():
    m = mines_en((0, 0))
    ouvert = grille(False)
    ouvert[1][1] = True
    jeu.ouvrir_autour(m, ouvert, grille(False), 1, 1)
    assert nb_vraies(ouvert) == 1, \
        ("(1, 1) affiche 1 mais il n'y a aucun drapeau autour : "
         "il ne doit rien se passer")


def test_ouvrir_autour_avec_le_bon_drapeau():
    m = mines_en((0, 0))
    ouvert, drapeaux = grille(False), grille(False)
    ouvert[1][1] = True
    drapeaux[0][0] = True
    jeu.ouvrir_autour(m, ouvert, drapeaux, 1, 1)
    assert not ouvert[0][0], "la case avec le drapeau ne doit pas s'ouvrir"
    assert ouvert[0][1] and ouvert[2][2], \
        "(1, 1) affiche 1 et a 1 drapeau autour : ses voisines doivent s'ouvrir"
    assert nb_vraies(ouvert) == jeu.LIGNES * jeu.COLONNES - 1, \
        ("les voisines ouvertes doivent lancer la cascade "
         "(utilise reveler)")


def test_ouvrir_autour_trop_de_drapeaux():
    m = mines_en((0, 0))
    ouvert, drapeaux = grille(False), grille(False)
    ouvert[1][1] = True
    drapeaux[0][1] = drapeaux[1][0] = True
    jeu.ouvrir_autour(m, ouvert, drapeaux, 1, 1)
    assert nb_vraies(ouvert) == 1, \
        ("(1, 1) affiche 1 mais a 2 drapeaux autour : il faut EXACTEMENT "
         "autant de drapeaux que le chiffre")


def test_ouvrir_autour_mauvais_drapeau():
    m = mines_en((0, 0))
    ouvert, drapeaux = grille(False), grille(False)
    ouvert[1][1] = True
    drapeaux[0][1] = True                # drapeau a cote de la vraie mine
    jeu.ouvrir_autour(m, ouvert, drapeaux, 1, 1)
    assert ouvert[0][0], \
        ("le drapeau est au mauvais endroit : la mine (0, 0) s'ouvre et "
         "on perd. C'est la regle du vrai demineur !")


def test_ouvrir_autour_case_fermee():
    m = mines_en((0, 0))
    ouvert, drapeaux = grille(False), grille(False)
    drapeaux[0][0] = True
    jeu.ouvrir_autour(m, ouvert, drapeaux, 1, 1)
    assert nb_vraies(ouvert) == 0, \
        "(1, 1) n'est pas ouverte : ouvrir_autour ne doit rien faire"


# ------------------------------------------------------------- lancement
ETAPES = [
    (1, "nouvelle_grille", [test_grille_dimensions,
                            test_grille_lignes_independantes]),
    (2, "dans_grille", [test_dans_grille]),
    (3, "voisins", [test_voisins_au_milieu, test_voisins_dans_un_coin]),
    (4, "compter_mines", [test_compter_mines]),
    (5, "poser_mines", [test_poser_mines_nombre_et_zone,
                        test_poser_mines_au_hasard]),
    (6, "basculer_drapeau", [test_drapeau_pose_et_enleve,
                             test_pas_de_drapeau_sur_case_ouverte]),
    (7, "reveler", [test_reveler_un_chiffre, test_reveler_en_cascade,
                    test_reveler_respecte_les_drapeaux,
                    test_reveler_une_mine]),
    (8, "a_gagne", [test_a_gagne, test_a_gagne_regarde_toute_la_grille]),
    (9, "case_cliquee", [test_case_cliquee_dans_la_grille,
                         test_case_cliquee_bords]),
    (10, "ouvrir_autour", [test_ouvrir_autour_sans_drapeau,
                           test_ouvrir_autour_avec_le_bon_drapeau,
                           test_ouvrir_autour_trop_de_drapeaux,
                           test_ouvrir_autour_mauvais_drapeau,
                           test_ouvrir_autour_case_fermee]),
]

NIVEAUX = {1: "NIVEAU 1 - remplir les ____",
           5: "NIVEAU 2 - ecrire les lignes manquantes",
           8: "NIVEAU 3 - ecrire la fonction entiere"}


def fonction_du_jeu(tb):
    """Nom de la derniere fonction du jeu traversee avant l'erreur."""
    nom = None
    for frame in traceback.extract_tb(tb):
        if os.path.basename(frame.filename) == nom_module + ".py":
            nom = frame.name
    return nom


def lancer(test):
    """Renvoie None si le test passe, sinon un message d'explication."""
    try:
        test()
        return None
    except AssertionError as erreur:
        return str(erreur)
    except NotImplementedError:
        return "pas encore ecrite (il y a toujours la ligne raise)"
    except RecursionError:
        return ("RecursionError : la fonction s'appelle elle-meme a l'infini. "
                "Qu'est-ce qui l'empeche de rouvrir une case deja ouverte ?")
    except NameError as erreur:
        _, _, tb = sys.exc_info()
        ou = fonction_du_jeu(tb)
        if "____" in str(erreur):
            return "il reste un trou ____ a remplir dans " + str(ou) + "()"
        return "NameError dans %s() : %s" % (ou, erreur)
    except Exception as erreur:
        _, _, tb = sys.exc_info()
        ou = fonction_du_jeu(tb)
        return "le programme a plante dans %s() : %s: %s" % (
            ou, type(erreur).__name__, erreur)


print("")
print("Tests de " + nom_module + ".py")
print("=" * 64)

validees = 0
prochaine = None
for numero, nom, tests in ETAPES:
    if numero in NIVEAUX:
        print("")
        print("  " + NIVEAUX[numero])
    messages = []
    for test in tests:
        message = lancer(test)
        if message is not None and message not in messages:
            messages.append(message)
    if not messages:
        validees += 1
        print("[ OK ] etape %2d  %s" % (numero, nom))
    elif prochaine is None:
        prochaine = (numero, nom)
        print("[FAIL] etape %2d  %s" % (numero, nom))
        for message in messages:
            print("         - " + message)
    else:
        print("[ .. ] etape %2d  %s" % (numero, nom))

print("")
print("=" * 64)
print("%d / %d etapes validees" % (validees, len(ETAPES)))
print("")
if prochaine is None:
    print("Tout est bon ! Lance le jeu :  python " + nom_module + ".py")
else:
    print("Au travail sur l'etape %d : %s()" % prochaine)
    print("[ .. ] = pas encore regarde : chaque chose en son temps.")
