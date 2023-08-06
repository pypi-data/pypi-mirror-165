# zpp-args
## Informations
Module pour le traitement des arguments d'une ligne de commande.
<br>Trois sources possibles:
- sys.argv
- une chaîne de caractère
- une liste

### Prérequis
- Python 3
<br>

# Installation
```console
pip install zpp_args
```

# Utilisation
### Conseil d'importation du module
```python
from zpp_args import parser
```
<br>

### Initialisation du parser
```python
parse = parser(SOURCE, error_lock=False)
```
>En paramètre supplémentaire, nous pouvons mettre:<br/>
>- error_lock: Purge le retour de la fonction si une erreur s'est produite (Par défaut: False)
<br>

### Initialisation des arguments
```python
parse.set_argument(NAME)
```
L'initialisation doit prendre au moins un des deux paramètres suivants:
- shortcut: Pour les arguments courts (1 caractère)
- longname: Pour les arguments explicites (1 mot ou ensemble de mots séparés par le symbole \_)

_Si non précisé, la fonction initialise shortcut_

>En paramètre supplémentaire, nous pouvons mettre:<br/>
>- error_lock: Purge le retour de la fonction si une erreur s'est produite (Par défaut: )
>- type: Pour forcer l'argument reçu à un str ou un digit (Par défaut: None)
>- default: Pour choisir une valeur par défaut(Par défaut: None)
>- description: Pour ajouter une description à l'argument à afficher lors de l'appel de la commande help(Par défaut: None)
>- required: Choisir si cet argument est nécessaire (Par défaut: False)
>- store: Choisir si l'argument' est un simple True/False ou s'il attends une variable (Par défaut: bool)
<br>

### Initialisation des paramètres
L'initialisation des paramètres va permettre d'agrémenter la commande help et de fixer une limite minimum lors de la récupération des paramètres
```python
parse.set_argument(NAME)
```
>En paramètre supplémentaire, nous pouvons mettre:<br/>
>- description: Pour ajouter une description au paramètre à afficher lors de l'appel de la commande help(Par défaut: None)
<br>

### Execution du parseur
```python
argument, parameter = parse.load()
```
Retourne une liste avec les paramètres et une classe (StoreArgument) avec les arguments
La StoreArgument peut retourner un dictionnaire en appelant argument.list_all()

<br>

### Initialisation de la description de la commande
```python
parse.set_description(DESCRIPTION)
```
<br>

### Affichage de l'aide
```python
parse.help()
```
<br>

### Désactiver le check sur les paramètres
Pour désactiver le check du nombre de paramètres à envoyer, il suffit d'appeler la fonction suivante.
```python
parse.disable_check()
```