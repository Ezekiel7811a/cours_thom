# Démineur — code à trous

## Le jeu

- Une grille de **9 lignes sur 12 colonnes**, avec **15 mines** cachées.
- **Clic gauche** : ouvrir une case.
  - Si c'est une mine, c'est perdu.
  - Sinon, la case affiche **le nombre de mines parmi ses 8 voisines**.
  - Si ce nombre est 0, les voisines s'ouvrent toutes seules, en cascade.
- **Clic droit** : poser ou enlever un drapeau (« ici, je pense qu'il y a une
  mine »). Une case avec un drapeau ne peut pas être ouverte par erreur.
- **Clic gauche sur un chiffre déjà ouvert** : si tu as posé autant de drapeaux
  autour que le chiffre, toutes les autres voisines s'ouvrent d'un coup.
- Le premier clic ne tombe jamais sur une mine.
- On gagne quand toutes les cases sans mine sont ouvertes.
- Touche **R** : nouvelle partie.

## Ta mission

Le fichier `demineur.py` est complet… sauf **10 fonctions** à qui il manque des
morceaux. Elles sont numérotées de l'**étape 1** à l'**étape 10**, et elles
deviennent de plus en plus dures :

| Niveau | Étapes | Ce qui manque |
|---|---|---|
| 1 | 1 à 4 | des expressions : remplace chaque `____` |
| 2 | 5 à 7 | des lignes entières (`________________`) |
| 3 | 8 à 10 | toute la fonction : il ne reste que son nom et sa description |

Tout le reste du fichier (le dessin, la souris) marche déjà.

## Comment travailler

```bash
python tests_demineur.py
```

Les tests te disent **quelle étape faire** et, quand ça ne marche pas,
**ce qui ne va pas**. La boucle :

1. Lis la description de la fonction (le texte entre `"""`).
2. **Avant d'écrire**, prends un exemple sur papier : « pour la case (0, 0), la
   fonction doit répondre… ».
3. Complète.
4. Lance les tests.
5. `[FAIL]` ? Lis le message, corrige, relance. `[ OK ]` ? Étape suivante.

Tu peux (et tu dois) utiliser les fonctions des étapes précédentes : c'est
pour ça qu'on les fait dans l'ordre.

## Le repère de la grille

```
            col 0   col 1   col 2  ...  col 11
          +-------+-------+-------+
  lig 0   | (0,0) | (0,1) | (0,2) |
          +-------+-------+-------+
  lig 1   | (1,0) | (1,1) | (1,2) |
          +-------+-------+-------+
  ...
  lig 8
```

Une case, c'est toujours **(ligne, colonne)**, et on y accède avec
`grille[lig][col]` : d'abord la ligne, ensuite la colonne. La grille n'est pas
carrée exprès : si tu inverses les deux, ça se verra.

Le jeu utilise trois grilles de même taille, remplies de `True` / `False` :

| Grille | `True` veut dire… |
|---|---|
| `mines` | il y a une mine sur cette case |
| `ouvert` | la case a été ouverte |
| `drapeaux` | il y a un drapeau sur cette case |

## Boîte à outils

Tu n'as pas besoin de tout connaître par cœur, mais tout ce qui suit sert
quelque part.

**Liste en compréhension**
```python
carres = [x * x for x in range(5)]        # [0, 1, 4, 9, 16]
```

**Comparaisons enchaînées**
```python
0 <= age < 18      # la même chose que : 0 <= age and age < 18
```

**Déballer un couple**
```python
a, b = 3, 7
for nom, note in [("Léa", 15), ("Tom", 12)]:
    print(nom, note)
```

**Tirer au hasard sans remise**
```python
import random
random.sample(["a", "b", "c", "d"], 2)    # par exemple ['d', 'a']
```

**Inverser un booléen**
```python
lumiere = not lumiere
```

**Division entière**
```python
17 // 5       # 3
-3 // 5       # -1  (arrondi vers le bas)
int(-3 / 5)   # 0   (arrondi vers zéro : attention !)
```

**Une fonction qui s'appelle elle-même (récursivité)**
```python
def compte_a_rebours(n):
    if n < 0:          # 1. le cas où on S'ARRÊTE
        return
    print(n)
    compte_a_rebours(n - 1)   # 2. le cas où on recommence, en plus petit
```
Sans le point 1, la fonction s'appelle à l'infini et Python s'arrête avec
`RecursionError`. L'étape 7 fonctionne exactement comme ça.

## Pour l'étape 9

La souris donne une position en **pixels**, dans la fenêtre. Le coin en haut à
gauche de la grille n'est pas au pixel (0, 0) :

```
(0,0) de la fenêtre
  +--------------------------------------
  |              HAUT = 70 pixels
  |        +-----+-----+-----
  | MARGE  |(0,0)|(0,1)|
  | = 20   +-----+-----+-----
  |        |(1,0)|        chaque case fait CELL = 40 pixels
```

Fais le calcul à la main pour deux ou trois clics avant d'écrire le code.

## Ta feuille de route

| Étape | Fonction | Fait | Ce que j'ai appris / ce qui m'a bloqué |
|---|---|---|---|
| 1 | `nouvelle_grille` | ☐ | |
| 2 | `dans_grille` | ☐ | |
| 3 | `voisins` | ☐ | |
| 4 | `compter_mines` | ☐ | |
| 5 | `poser_mines` | ☐ | |
| 6 | `basculer_drapeau` | ☐ | |
| 7 | `reveler` | ☐ | |
| 8 | `a_gagne` | ☐ | |
| 9 | `case_cliquee` | ☐ | |
| 10 | `ouvrir_autour` | ☐ | |

Objectif final : **10 / 10 étapes validées**, puis une partie gagnée.
