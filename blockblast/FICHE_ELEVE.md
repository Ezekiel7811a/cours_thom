# Block Blast — chasse aux bugs

## Le jeu, tel qu'il devrait marcher

- Une grille de **8 cases sur 8**.
- **3 pièces** en bas de l'écran. On les attrape à la souris et on les pose
  dans la grille.
- Dès qu'une **ligne** ou une **colonne** est entièrement remplie, elle explose
  et rapporte des points.
- Quand les 3 pièces sont posées, 3 nouvelles arrivent.
- La partie est finie quand **aucune** des pièces restantes ne rentre nulle part.
- Touche **R** : nouvelle partie.

## Le problème

Le fichier `blockblast.py` contient **8 bugs volontaires**. Rien n'est marqué
dans le code : à toi de les trouver et de les réparer.

Il y a 3 bugs faciles, 3 moyens et 2 difficiles.

## Tes deux outils

**1. Jouer.**

```bash
python blockblast.py
```

Garde la fenêtre du terminal visible à côté du jeu : certains bugs y écrivent
des messages d'erreur.

**2. Les tests automatiques.**

```bash
python tests_blockblast.py
```

Ils appellent les fonctions du jeu une par une et vérifient leurs réponses.
Chaque test raté te dit **ce qui ne va pas** et **où chercher**.

Attention : les tests ne voient pas tout. **6 bugs sur 8** sont détectés par
les tests. Les 2 derniers ne se voient qu'en jouant.

## La méthode (à suivre dans l'ordre, à chaque bug)

1. **Reproduire.** Quelle action exacte déclenche le problème ? Si tu ne sais
   pas le refaire à volonté, tu ne pourras pas vérifier ta correction.
2. **Décrire.** Écris en une phrase ce que tu vois, et ce que tu devrais voir.
3. **Localiser.** Quelle fonction s'occupe de ça ? Le nom des fonctions est en
   français, lis-les toutes une fois avant de commencer.
4. **Comprendre.** Relis la fonction ligne par ligne. Ajoute des `print()` pour
   voir la valeur des variables :
   ```python
   print("lig =", lig, " col =", col)
   ```
5. **Corriger** — une seule chose à la fois.
6. **Vérifier.** Relance les tests **et** le jeu. Une correction peut en casser
   une autre.
7. Enlève tes `print()` quand c'est réglé.

## Lire un message d'erreur

Quand Python affiche du rouge dans le terminal, ça ressemble à ça :

```
Traceback (most recent call last):
  File "blockblast.py", line 88, in peut_placer
    if grille[l][c] is not None:
IndexError: list index out of range
```

Ça se lit **de bas en haut** :

- dernière ligne = **le type d'erreur** (ici : un indice de liste trop grand) ;
- juste au-dessus = **le fichier, le numéro de ligne et la fonction** ;
- le reste = qui a appelé qui pour en arriver là.

Le numéro de ligne, c'est là où ça a *explosé*. Ce n'est pas toujours là où est
la *cause* — mais c'est toujours le bon endroit où commencer à regarder.

## Les fonctions du jeu

| Fonction | Ce qu'elle fait |
|---|---|
| `nouvelle_grille()` | crée une grille 8×8 vide |
| `nouvelle_piece()` | tire une pièce au hasard |
| `taille_piece(p)` | hauteur et largeur d'une pièce |
| `peut_placer(...)` | dit si une pièce rentre à un endroit donné |
| `placer(...)` | écrit la pièce dans la grille |
| `lignes_completes(g)` | trouve les lignes et colonnes pleines |
| `effacer(...)` | vide les lignes et colonnes pleines |
| `partie_finie(...)` | dit si on est bloqué |
| `case_visee(...)` | convertit la position de la souris en (ligne, colonne) |
| `dessiner()` | redessine tout l'écran |
| `souris_relachee(e)` | ce qui se passe quand on lâche une pièce |

Dans tout le programme, une case se repère par `grille[ligne][colonne]`.
La ligne 0 est **en haut**, la colonne 0 est **à gauche**.

## Ta feuille de route

Coche au fur et à mesure. Pour chaque bug, note le symptôme et la correction.

| # | Symptôme observé | Fonction | Correction |
|---|---|---|---|
| 1 | | | |
| 2 | | | |
| 3 | | | |
| 4 | | | |
| 5 | | | |
| 6 | | | |
| 7 | | | |
| 8 | | | |

Objectif final : **11 / 11 tests réussis** et une partie qui se joue sans rien
de bizarre.
