<!--- 
# Université de Montréal
# IFT-6758-A  -  A23  -  Science des données
-->

# Devoir 6

Évaluation de l'assignation :

| Composant                                                   | Fichiers Requis   | Note |
|-------------------------------------------------------------|------------------|:-----:|
| Code (5 fonctions)                                          | `nlp_code.py`    |  50   |
| &emsp;+ figures, exécutions de cellules, sorties            | `hw6.ipynb`      |  10   |
| rapport (T1.3, T3 1-3, T4.4, T5)                            | `hw6.pdf`        |  40   |



Une partie de votre devoir sera automatiquement notée, c'est-à-dire que vous ne devez **pas modifier la signature des fonctions définies** (mêmes entrées et sorties).

### Soumission

Pour soumettre les fichiers, veuillez soumettre **uniquement les fichiers requis** (listés dans le tableau ci-dessus) que vous avez complétés à **gradescope**; n'incluez pas les données ou autres fichiers divers.

**Attention 1: Vérifiez attentivement comment j'ai défini les fonctions et leurs sorties attendues.**

**Attention 2: Je vous demande d'effectuer certaines actions dans le cahier jupyter, ne les sautez pas. Si je suis suspicieux quant à votre travail, je vérifierai si vous avez suivi mes instructions.**

**Attention 3: Pour la tâche 5, vous devrez implémenter un modèle de transformateur. Je vous recommande de faire cette partie dans Google Colab et d'utiliser un environnement d'exécution qui utilise des GPU (Vous pouvez déboguer votre implémentation sur le CPU, puis effectuer l'entraînement sur l'environnement d'exécution GPU).**

**Attention 4: distilBERT nécessite un format spécifique pour ses entrées. Vous devrez changer le nom des colonnes de l'ensemble de données en "text" et "labels" sinon cela ne fonctionnera pas. De plus, je veux que vous gardiez les divisions d'entraînement et de test fournies dans les sections précédentes et que vous travailliez avec les critiques prétraitées et les étiquettes encodées (il est judicieux de les enregistrer sous forme de fichiers CSV que vous pourrez utiliser ultérieurement).**

**Attention 5: Je n'accepterai pas les réponses oui/non ou les réponses minimales pour le rapport. Étayez votre analyse avec les graphiques demandés et utilisez des références lorsque cela est nécessaire.**

**Attention 6: Dans votre rapport, incluez votre nom et votre numéro d'étudiant. Si une tâche comporte des questions auxquelles vous devez répondre ou quelque chose que vous devez discuter ou expliquer, veuillez ajouter un titre indiquant la section rapportée de l'assignation, puis vos réponses/discussions.**

## Tâche 1: Préparation des Données et Exploration Initiale

Nous commencerons par charger nos données et vérifier leur forme et leur contenu général. Vous devrez vérifier les valeurs NaN et les lignes en double et les gérer correctement (c'est-à-dire en conservant la première apparition et en supprimant les autres). Assurez-vous de vérifier que nous travaillons avec des points de données uniques. 

- Compléter les opérations requises pour répondre aux questions du rapport `hw6.ipynb`
- Répondre dans votre rapport aux questions suivantes `hw6.pdf` :

* Nombre de datapoints (?)
* Combien de valeurs uniques notre colonne cible contient-elle?
* Contient-il des valeurs NaN?
* Y a-t-il des critiques en double? (Si vous trouvez des lignes en double, combien de doublons avez-vous trouvés? 

## Tâche 2: Prétraitement des Données

- Compléter `nlp_code.py:preprocess_text()`
- Compléter les opérations requises dans le cahier `hw6.ipynb`

Dans cette section, nous prétraiterons nos critiques. Vous devrez compléter la fonction `preprocess_text()` qui prend une seule chaîne de caractères et la formate. Vous appliquerez cette fonction à toutes les critiques.

## Tâche 3: Analyse Exploratoire des Données (EDA)

Dans cette section, nous effectuerons une analyse exploratoire des données et répondrons à certaines questions sur nos critiques et notre ensemble de données. Assurez-vous de faire les opérations nécessaires et d'étayer votre réponse avec les supports nécessaires.

- Compléter `nlp_code.py:review_lengths()`
- Compléter `nlp_code.py:word_frequency()`
- Compléter les opérations requises dans le cahier `hw6.ipynb`
- Répondre dans votre rapport aux questions suivantes et étayez-les avec les graphiques et analyses nécessaires `hw6.pdf` :

* Comment les valeurs cibles sont-elles distribuées ? Avons-nous un ensemble de données presque équilibré ?
* Toutes les critiques ont-elles la même longueur ?
* Quelle est la longueur de séquence moyenne ?
* Quels sont les 20 mots les plus fréquents ?
* Quels sont les 20 mots les moins fréquents ?
* Après avoir effectué certaines analyses exploratoires des données (EDA), pensez-vous qu'il sera facile de classifier ces critiques ? Pourquoi oui ? Pourquoi non ?

## Tâche 4 : Extraction de caractéristiques et préparation de la cible

Dans cette section, nous encoderons notre colonne cible (vous devrez implémenter la fonction `encode_sentiment()`, en faisant attention au type de données de la "sentiment" encodée) et réaliserons une extraction de caractéristiques avec un vecteur TF-IDF. Nous entraînerons un modèle simple et l'utiliserons comme référence pour comprendre la difficulté de classifier les critiques. Enfin, vous découvrirez un nouvel outil d'explicabilité de modèle appelé LIME (vous devrez compléter la fonction `explain_instance()`).

- Complétez `nlp_code.py:encode_sentiment()`
- Complétez `nlp_code.py:explain_instance()`
- Effectuez les opérations requises dans le notebook `hw6.ipynb`
- Répondez dans votre rapport aux questions suivantes en les étayant avec les graphiques et analyses nécessaires dans `hw6.pdf` :

TF-IDF (Term-frequency times inverse document-frequency) :

* Expliquez les inconvénients de l'utilisation de cette méthode.
* Proposez une méthode alternative que nous aurions pu utiliser pour obtenir une meilleure représentation numérique des mots présents dans notre corpus. (Pourquoi pensez-vous que cela pourrait fonctionner mieux ?)

LIME (Local Interpretable Model-agnostic Explanations) :

Ajoutez dans votre rapport la visualisation obtenue et fournissez une interprétation.

## Tâche 5 : Exploration d'un modèle transformateur

- Implémentez le modèle distilBERT et obtenez les scores et la visualisation requis : `hw6.ipynb`
- Laissez des traces de votre implémentation dans le notebook Jupyter : `hw6.ipynb`

1-. Implémentez le modèle `distilBERT`, entraînez-le et évaluez-le sur le même ensemble d'entraînement que notre classificateur Naïve Bayes. Vous pouvez sauvegarder les ensembles de données prétraités en fichiers `csv` (avec les noms de colonnes `text` et `labels`) et les charger ensuite en utilisant la méthode `load_dataset` de la bibliothèque `datasets`. Faites attention au formatage des entrées pour ce modèle transformateur (son nom est : `distilbert-base-uncased`).

- Répondez dans votre rapport aux questions suivantes en les étayant avec les analyses, scores et visualisations nécessaires dans `hw6.pdf` :

2-. Explorez 2 différentes façons de régler le modèle (# epochs, taux d'apprentissage, décroissance du poids, etc.) pour améliorer les performances de classification (au point 3, vous rapporterez les résultats pour le meilleur modèle). Je veux connaître en détail la méthodologie que vous avez suivie pour améliorer les performances du modèle. Par conséquent, j'attends une discussion raisonnable sur les approches que vous avez prises (je pénaliserai le changement aléatoire des hyperparamètres du modèle).

3-. Vous devrez inclure dans votre rapport votre précision, votre rappel et vos scores F1 (Discutez ce que signifie qu'un modèle est meilleur qu'un autre, qu'est-ce que ces scores signifient ?). Incluez également l'image de votre matrice de confusion sous forme de carte thermique. Rapportez si les résultats obtenus sont nettement meilleurs que ceux obtenus avec le classificateur Naïve Bayes (étayez vos commentaires en comparant les scores et les cartes thermiques, j'attends une discussion approfondie).
