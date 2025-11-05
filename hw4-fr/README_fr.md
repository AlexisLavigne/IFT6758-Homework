# Devoir $5$

Barème de notation :

| Section                       | Note  |
|-------------------------------|:-----:|
| Question 1                    |  40   |
| Question 2                    |   5   |
| Question 3                    |  10   |
| Question 4                    |   6   |
| Question 5                    |   6   |
| Question 6                    |  10   |
| Question 7                    |  10   |
| Question 8                    |   8   |
| Question 9                    |   5   |

<!-- Cela devrait totaliser 100 -->

En général, vos devoirs seront notés automatiquement, c'est-à-dire que vous **ne devez pas** modifier la signature des fonctions définies (mêmes entrées et sorties).

## Contexte

L'objectif de cet exercice est d'acquérir de l'expérience avec un fournisseur de services cloud (dans ce cas, Google Cloud) afin de créer et déployer des applications de machine learning.

En particulier, nous allons travailler avec [Google Cloud Build](https://cloud.google.com/build) pour construire notre application sous forme d’images Docker et les stocker dans un dépôt distant (appelé [Google Artifact Registry](https://cloud.google.com/artifact-registry)).

Notre application se compose d'un composant backend (application Flask) et d'un composant frontend (application Streamlit) qui seront construits dans des images Docker distinctes. Le frontend nous permettra de soumettre une URL d'image, qui sera envoyée au backend pour classification par un modèle de ML.

Nous allons ensuite utiliser [Google Cloud Run](https://cloud.google.com/run) pour déployer chaque composant de l'application sur le web.

Il vous sera demandé d'écrire le code et les fichiers de configuration nécessaires pour :
- Soumettre des builds à Google Cloud Build
- Déployer chaque composant sur Google Cloud Run

Il y aura également des questions à réponses courtes. Écrivez et soumettez vos réponses dans `SHORT_ANSWER_TEMPLATE.md`.

### 0. Créer un compte Google Cloud
Si vous n'avez pas encore de compte Google Cloud, vous pouvez en créer un [ici](https://console.cloud.google.com).

Les vidéos suivantes fournissent un aperçu de certains concepts clés lors de l'utilisation de Google Cloud :
- Comment s'inscrire à Google Cloud -- [lien](https://youtu.be/ogzJovMsDIU?si=VCZ16ONz0CYvbGBV&t=40)
- Comment naviguer dans Google Cloud -- [lien](https://youtu.be/27Pb5g7bEAA?si=yuuDIv_4nzJL2tLd&t=75)

### 1. Créer un projet Google Cloud
Créez un projet Google Cloud avec les informations suivantes :

- Nom du projet : `hw5-STUDENT_ID`
- ID du projet : `hw5-STUDENT_ID`

Assurez-vous que le nom et l'ID du projet soient **identiques**. **Vous ne pouvez pas modifier l'ID du projet par la suite. Le nom et l'ID sont sensibles à la casse.**

Exemple : Si mon ID étudiant est 123456789, alors mon nom de projet sera :
`hw5-123456789` et mon ID de projet sera : `hw5-123456789`.

### 2. Installer l’interface en ligne de commande gcloud
L'interface en ligne de commande de Google Cloud (gcloud) est un "ensemble d'outils pour créer et gérer des ressources Google Cloud" ([source](https://cloud.google.com/sdk/gcloud)). L'utilisation de gcloud est nécessaire pour interagir avec Google Cloud depuis votre machine.

Les instructions pour installer gcloud se trouvent [ici](https://cloud.google.com/sdk/docs/install).

Une fois gcloud installé, utilisez-le pour configurer votre projet :
```
gcloud config set project MY_PROJECT_ID
```
où `MY_PROJECT_ID` est l'ID du projet créé à l’étape 1.

Vous pouvez vérifier que vous êtes bien sur le bon projet en exécutant la commande suivante :
```
gcloud config list
```

### 3. Activer les API
Les API suivantes doivent être activées pour votre projet :
- API de l’Artifact Registry
- API Cloud Run
- API Cloud Build

Vous pouvez activer ces API en exécutant la commande suivante :
```
gcloud services enable artifactregistry.googleapis.com run.googleapis.com cloudbuild.googleapis.com
```

### 4. Créer un dépôt Docker sur l'Artifact Registry
Un dépôt Docker est nécessaire pour stocker les images Docker que nous allons construire avec Google Cloud Build. Sur Google Cloud, un dépôt Docker est hébergé sur l'Artifact Registry.

Vous pouvez créer un dépôt sur l'Artifact Registry en exécutant la commande suivante :
```
gcloud artifacts repositories create REPO_NAME \
    --repository-format=docker \
    --location=LOCATION \
    --project=PROJECT_ID
```

Assurez-vous de configurer les éléments suivants :
- REPO_NAME : `hw5-images`
- LOCATION : `us-central1`
- PROJECT_ID : l'ID du projet créé à l’étape 1.

Vous pouvez vérifier que votre dépôt a bien été créé en exécutant la commande suivante :
```
gcloud artifacts repositories list --project=PROJECT_ID
```

### 5. Vérifier les prérequis
Avant de commencer cet exercice, assurez-vous d'avoir complété toutes les étapes listées ci-dessus.

Pour vérifier que votre projet est correctement configuré, exécutez la commande suivante :
```
./setup/check_prereq.sh
```

Si toutes les vérifications sont réussies, vous verrez la sortie suivante :
```
All prerequisites are met. You can proceed with the assignment.
```

Si vous voyez des erreurs, assurez-vous de les corriger avant de continuer.

# Questions

## 1. Question 1
La première étape consistera à créer un fichier YAML Cloud Build, qui détermine les étapes nécessaires pour construire notre image Docker et la pousser vers l'Artifact Registry.

### Création d'un fichier YAML Cloud Build
Construisez un fichier YAML Cloud Build en utilisant le fichier `deployment/cloudbuild_template.yaml` comme modèle.

Dans ce fichier, nous allons utiliser des substitutions pour remplir les valeurs correctes. Les substitutions permettent de passer des variables dans le processus de build.

En regardant `deployment/submit_build_template.sh`, les substitutions suivantes sont disponibles :
- `_BASE_IMAGE_URI`
- `_APP_URI` (l'URI de l'image que nous construisons)
- `_SERVING_PORT`
- `_DOCKERFILE`

qui peuvent être référencées sous la forme `${SUBSTITUTION_NAME}` dans votre fichier YAML.

Il y a également `${BUILD_ID}` qui est une variable d'environnement présente dans Google Cloud Build et qui contient la valeur de l'identifiant de build unique actuel.

Vous devrez remplir les valeurs correctes pour vous assurer que ces substitutions sont correctes. Voir `#FILL ME IN` dans le fichier `deployment/submit_build_template.sh`.

Suivez les instructions dans `deployment/cloudbuild_template.yaml` pour créer un fichier YAML Cloud Build qui construira et poussera notre image Docker.

Dans le fichier Cloud Build, nous construisons deux images :
- Une image de "base" contenant toutes nos dépendances.
- Une deuxième image qui est construite à partir de notre image de base et qui installe notre code.
Nous explorerons pourquoi dans la question suivante.

Plus d'informations sur la création d'un fichier YAML Cloud Build se trouvent [ici](https://cloud.google.com/build/docs/configuring-builds/create-basic-configuration).

**ASTUCE :** Assurez-vous de lire et comprendre les fichiers Docker que vous construisez. Ces fichiers Docker utilisent l'instruction `ARG`, qui vous obligera à passer les bonnes valeurs lors de la soumission du build. Voir [Build Variables](https://docs.docker.com/build/building/variables/) pour plus d'informations.

### Soumission du build à Cloud Build
Une fois que vous avez créé le fichier Cloud Build, utilisez la commande `gcloud` pour soumettre le build à Cloud Build. Vous pouvez utiliser le fichier `submit_build_template.sh` pour cela. Plus de documentation sur `gcloud builds` se trouve [ici](https://cloud.google.com/sdk/gcloud/reference/builds/submit).

Lorsque vous exécutez le script, vous verrez les logs s'afficher dans le terminal. `gcloud` vous donnera également un lien pour visualiser le build dans votre navigateur. Vous pouvez consulter tous vos builds [ici](https://console.cloud.google.com/cloud-build/builds).

### Livrables
Pour cette question, vous devez soumettre les fichiers suivants :
- 1 fichier YAML Cloud Build.
- 1 script de soumission de build.
- Fichier `deliverables.yaml` avec les identifiants de build pour les builds du backend et du frontend.

## 2. Question 2
Combien d'images sont construites à chaque fois que vous soumettez un build ?
Cela doit-il toujours être le cas ? Pourquoi ou pourquoi pas ?
Si non, comment pourriez-vous accélérer le processus de build ?
Ajoutez une étape au début de vos fichiers Cloud Build pour résoudre cette inefficacité.

**Indice :** Voir [Meilleures pratiques pour accélérer les builds](https://cloud.google.com/build/docs/optimize-builds/speeding-up-builds).

## 3. Question 3
Une fois que nous avons construit et poussé nos images Docker, nous pouvons les déployer en utilisant le service Google Cloud Run.
Cette question se concentre sur le déploiement des services `backend_v1` et `frontend_v1`. Tous vos services Google Cloud Run peuvent être consultés [ici](https://console.cloud.google.com/run).

Vous pouvez utiliser le fichier `deployment/deploy_service_template.sh` pour commencer.

Lorsque vous déployez votre service frontend, assurez-vous de spécifier une variable d'environnement, `SERVING_URL`, qui est l'URL du service backend.

Vous devrez également connaître l'URI de l'image que vous souhaitez déployer. Vous pouvez les trouver dans l'Artifact Registry, situé [ici](https://console.cloud.google.com/artifacts). Cela devrait ressembler à ceci :

![](_assets/artifact_registry.png)

En cliquant sur les trois points à côté de l'image souhaitée, et en sélectionnant "Afficher la commande de pull", vous pouvez obtenir l'URI complet de l'image.

Une fois que vous exécutez le script, vous verrez l'URL du service déployé dans le terminal. Chaque service (frontend et backend) aura une URL différente. Une fois que les deux services sont déployés, vous pouvez les tester en accédant à l'URL du frontend et en téléchargeant une image.

Incluez deux scripts dans votre soumission :
- `deploy_backend_v1.sh`
- `deploy_frontend_v1.sh`
- Incluez l'URL du service déployé dans `deliverables.yaml`.

## 4. Question 4
Lorsque `backend_v1` est déployé, vous remarquerez dans les logs qu'il télécharge le modèle ResNet depuis le hub PyTorch. Cela prendra du temps.

Quelles sont les façons de contourner cela ?
Cela affectera-t-il le processus de build ? Si oui, comment ?

## 5. Question 5
Nous avons déployé les services backend et frontend séparément.
Quels sont les avantages et les inconvénients de cette approche ?

## 6. Question 6
Déployez les services `backend_v2` et `frontend_v2` en créant deux nouveaux services Cloud Run : `backend_v2` et `frontend_v2`.

Lorsque vous déployez votre service frontend, assurez-vous de spécifier une variable d'environnement, `SERVING_URL`, qui est l'URL du service backend.

Vous pouvez utiliser le fichier `deploy_service_template.sh` pour commencer.
Incluez deux scripts dans votre soumission :
- `deploy_backend_v2.sh`
- `deploy_frontend_v2.sh`
- Incluez l'URL du service déployé dans `deliverables.yaml`.

Dans cette application, nous pourrons sélectionner différents modèles à utiliser pour la classification.

## 7. Question 7
Si vous regardez `backend_v1/app.py` et `backend_v2/app.py`, vous verrez que les modèles sont chargés dans une variable globale appelée `model`.

Dans le cas de notre application `v1`, pourquoi cela n'est-il pas vraiment un problème ?
Dans `v2`, pourquoi est-ce un problème (Indice : que se passe-t-il si deux personnes utilisent l'interface en même temps) ?

Que devrions-nous modifier pour corriger cela ?
- Dans le frontend ? (Indice : Lisez [cet article](https://testdriven.io/blog/flask-sessions/))
- Dans le backend ?
    - Indice : Quelles sont les implications de charger le modèle choisi à chaque requête ? Avoir plusieurs modèles dans le même conteneur est-il une bonne idée ? Pourquoi ou pourquoi pas ?

## 8. Question 8
Inspectez le code dans `v3/`. Vous n'avez pas besoin de le construire et de le déployer (en fait, certaines parties sont incomplètes). Qu'essaie-t-il d'accomplir ? En quoi est-il différent des versions précédentes ? (Indice : Qu'est-ce qu'une passerelle API ?)

### 9. Question 9
"La quantification est le processus de réduction de la précision d'un signal numérique, généralement d'un format à haute précision à un format à plus faible précision. Cette technique est largement utilisée dans divers domaines, notamment le traitement du signal, la compression de données et le machine learning" ([source](https://www.ibm.com/think/topics/quantization)).

Quels sont les avantages et les inconvénients de l'utilisation de la quantification en ce qui concerne l'inférence de modèles ?

**Vous devez citer toutes les sources utilisées pour répondre à cette question.**
