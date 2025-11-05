# HW5 Short Answers


**Name:** Alexis Lavigne

**Matricule \#:** 20187363

## Question 2

À chaque fois qu'on soumet un *build*, deux images sont construites.
- D'abord, une image de base avec les dépendances communes
- Ensuite, une image de l'application (*target*) (frontend ou backend), créée à partir de l'image de base

Par contre, cela n'a pas toujours besoin d'être le cas. En effet, si on ne change pas l'image de base, on n'a pas besoin de la reconstruire à chaque fois avec une étape de *build* supplémentaire. On peut simplement réutiliser la dernière version (*latest*) déjà poussée dans le registre. On peut faire cela avec la commande *pull*, mais il faut évidemment l'avoir construite et l'avoir *push* sur le registre au moins une fois avant. Cela permet d'utiliser le cache de l'image précédente, donc d'accélérer le processus du build, car on ne doit pas reconstruire une image de base à chaque fois.

## Question 4

Une des façons de coutourner le problème de téléchargement du modèle ResNet au démarrage du service est de déplacer cette étape dans le *build* du backend_v1 à la place du déploiement. Donc, le Dockerfile du backend devrait contenir des étapes qui téléchargent et sauvegardent le modèle ResNet pendant la construction de l'image. 

Cela rendera le *build* plus long et plus lourd, mais une fois que l'image sera construite, le démarrage de notre service et les inférences seront plus rapides, car le modèle sera déjà présent dans l'image. En d'autres mots, à la place de le télécharger à chaque fois qu'on démarre le service, il sera fait uniquement une fois lors du build. 

Une autre façon serait de stocker le modèle, dans Artifact Registry ou Google Cloud Service par exemple, pour pouvoir le réutiliser sans avoir besoin de le rétélécharger à chaque fois.


## Question 5

Voici les avantages d'avoir les services backend et frontend séparés:
- Les deux sont complètement isolés, ce qui améliore la sécurité, la mise à l'échelle et la maintenabilité puisqu'ils sont tous indépendants. 
- Chaque service est déployé ou mise à jour indépendamment. Par exemple, si on fait un changement dans le backend, on ne doit pas tout redéployer, on doit juste redéployer le backend (le frontend reste inchangé). 
- Il y a une meilleure résilience. S'il y a une erreur, elle n'affectera pas toute l'application. En effet, on peut juste faire un *rollback* sur un seul service sans impact sur l'autre. 
- On peut aussi allouer les ressources de manière plus efficace. Si le backend a besoin de plus de ressources, on peut le mettre à l'échelle sans toucher au frontend. 
- De plus, en industrie (dans mon expérience), on a souvent deux équipes différentes qui travaillent indépendamment sur le frontend et sur le backend.

Voici les désavantages:
- La communication entre le frontend et backend est plus complexe. Il faut gérer les URLs, l'authentification, les permissions, etc.
- En étant séparés, il peut y avoir plus de délais sur le réseau entre les deux services.
- Il faut aussi faire attention aux vulnérabilités. Par exemple, avec HTTPS ou avece les clés de nos APIs. Cela ajoute de la configuration qui est parfois complexe.

Source : [IT Chronicles - 7 Splendid Reasons to Keep Frontend and Backend Separate](https://itchronicles.com/software-development/7-splendid-reasons-to-keep-frontend-and-backend-separate/)

## Question 7

Pour l'application v1, ce n'est pas un problème de charger le modèle dans une variable globale, car il y en a qu'un seul (ResNet). Donc, lorsque le service est déployé, toutes les requêtes vont utiliser le modèle ResNet (il n'y a pas le choix de sélection du modèle). Il y a donc pas de risque d'interférence entre différents utilisateurs.

Pour l'application v2, cela devient un problème, car on peut choisir un modèle (pas juste ResNet). Si le modèle est stocké dans une variable gloable, que deux utilisateurs utilisent le service, et que l'un des deux change de modèle, cela changera le modèle pour les deux (global). Cela n'est évidemment pas souhaitable et devient un gros problème quand il y a plus qu'un utilisateur qui utilise le service en même temps.

Pour modifier ce problème, pour le frontend, on peut utiliser les sessions. La session d'un utilisateur contiendra le modèle sélectionné pour chaque utilisateur (elle est spécifique à cet utilisateur). Lorsqu'il soumettera une image, cette variable de session sera envoyée dans la requête pour dire au backend d'utiliser ce modèle. Puis, lorsque l'utilisateur sélectionne un modèle différent, cette variable de session sera mise à jour. 

Pour le backend, il ne faudra pas utiliser une variable globale. Il faudra téléchargé le modèle dépendamment de celui qui a été sélectionné par l'utilisateur (inclut dans la requête). Par contre, le fait de devoir télécharger un modèle à chaque requête n'est pas très efficace et augmente le temps d'inférence. De plus, avoir plusieurs modèles dans le même conteneur n'est pas une bonne idée puisque ça rend le conteneur plus lourd, moins flexible et moins efficace. Il serait mieux de séparer les modèles dans des services ou conteneurs différents.

Source : [Testdriven.io - Sessions in Flask](https://testdriven.io/blog/flask-sessions/)

## Question 8

La nouvelle application v3 ajoute une nouvelle couche pour centraliser la communication entre le frontend et le backend. Cette nouvelle couche est l'API Gateway (passerelle API). Dans les autres applications (v1, v2), le frontend envoyait directement ses requêtes au backend, mais maintenant les requêtes passent d'abord par un API Gateway. 

En effet, voici un exemple d'une requête POST depuis le frontend qui est envoyée à BASE_URL/... où BASE_URL = API_GATEWAY si API_GATEWAY est défini comme variable d'environnement:

    return requests.post(f"{BASE_URL}/model/{model_id}/predict", json=dict(url=image_url))

Dans cette requête, on voit aussi que la requête est redirigée vers le bon modèle de prédiction avec */model_id*.

En général, un API Gateway permet de centraliser toute la gestion des requêtes, et peut donc gérer le routage, la journalisation, l'authentification (s'il y en a). Il peut aussi simplifier la communication, si on a plusieurs backends pour différents modèles par exemple. De plus, il rend l'architecture plus modulaire, et plus stable puisqu'il peut aussi distribuer les requêtes vers différentes instances de nos services (si on a un grand nombre d'utilisateurs). 

Source : [RedHat - What does an API gateway do?](https://www.redhat.com/en/topics/api/what-does-an-api-gateway-do)

## Question 9

Voici les avantages d'utiliser la quantification pour l'inférence de modèles:
- Réduction de la taille du modèle à télécharger (moins de mémoire). Le déploiement est alors plus rapide.
- Le temps d'inférence est plus rapide, moins de délais, car les calculs ont moins de précisions. 
- C'est aussi moins lourd et moins énergivore sur les ressources d"une machine (ex: moins de RAM)

Les désavantages:
- Il peut y avoir une perte d'exactitude et une perte de performance, car on effectue les calculs avec moins de précision (ex: passer de FP32 à INT8)
- Ça peut devenir plus complexe. En effet, la calibration ou la conversion des poids peut être couteuse et peut nécessiter beaucoup de données. 

Source : [IBM - What is quantization?](https://www.ibm.com/think/topics/quantization)
