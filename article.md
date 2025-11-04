# LocalStack : Développer et Tester vos Lambda Functions en Local

Dans un de nos  projet, on a un backend assez particulier : du full SQL avec Hasura en proxy devant. C'est super efficace pour les requêtes classiques, mais parfois on a besoin de faire des trucs plus complexes en Python.
Et c'est là qu'AWS Lambda entre en jeu.

Le problème ? Un developpement directement sur AWS, ça peut etre long et couter cher. Si vous devez passer par une équipe devops pour chaque modif, ça devient vite un cauchemar. Et vous ne pouvez pas tester localement. **LocalStack a changé la donne** : on peut maintenant développer et tester nos Lambdas en local

Cet article vous montre comment on a mis cette stack en places et les problèmes qu'on a rencontrés (spoiler : les Lambda Layers sur LocalStack, c'est payant).

## Lambda, c'est quoi exactement ?

AWS Lambda, c'est du **serverless**: un service de calcul qui exécute du code sans qu'il soit nécessaire de gérer des serveurs. Vous écrivez du code, AWS l'exécute quand il faut, et vous payez uniquement le temps d'exécution.

Et derriere c'est grosso-modo juste une fonction

```python
def lambda_handler(event, context):
    # event contient les données d'entrée
    # context donne des infos sur l'exécution
    return {
        'statusCode': 200,
        'body': json.dumps({'message': 'Hello from Lambda!'})
    }
```

Dans notre cas, on utilise les Lambdas pour :
- Communiquer avec des S3
- Envoyer des emails via des CRONs
- Faire des calculs qui prendraient trop de temps en SQL

On peut créer des lambdas via l'interface, soit par ligne de commande, c'est galère. Il faut définir l'infrastructure, gérer les permissions, déployer le code...

C'est là que **SAM** devient indispensable.

## SAM : Infrastructure pour les non devops

AWS SAM (Serverless Application Model), c'est un framework qui simplifie drastiquement la création de Lambdas. Tout se fait via un fichier YAML.

Un projet SAM ressemble à ça

```
mon-projet/
├── template.yaml          # Définit toute l'infrastructure
├── samconfig.toml         # Config de déploiement
├── src/handlers/          # Votre code Python
└── layers/                # Code partagé entre Lambdas
```

Le fichier **template.yaml** est le cœur du projet. Voici un exemple minimaliste :

```yaml
AWSTemplateFormatVersion: '2010-09-09'
Transform: AWS::Serverless-2016-10-31

Resources:
  HelloWorldFunction:
    Type: AWS::Serverless::Function
    Properties:
      FunctionName: hello-world-function
      CodeUri: src/handlers/hello_world/
      Handler: app.lambda_handler
      Runtime: python3.12
      Events:
        HelloWorld:
          Type: Api
          Properties:
            Path: /hello
            Method: get
```

C'est tout ! SAM va créer la Lambda Avec une simple commande

```bash
sam build   # Build le projet
sam deploy  # Déploie sur AWS
```

Bien sur, vous pouvez ajouter des S3, des API Gateway, des permissions IAM, tout est géré dans le YAML. Nous n'allons pas nous étendre là-dessus, les docs SAM sont très complètes (meme si bon courage pour trouver facilement l'information).

--------------- TODO ---------------
Expliquez comment SAM sait où deployer. Pas trouvé l'info facilement.
-----------------------------------------------

Bon, c'est cool, mais ça ne répond toujours pas à une problématique. A chaque fois qu'on veut tester, il faut déployer sur une vrai instante.  **LocalStack** résout ce problème.

## LocalStack : AWS sur votre machine

LocalStack is a cloud service emulator that runs in a single container on your laptop or in your CI environment.

- **Gratuit** : Pas de facture AWS qui explose. Mais des features premiums (nous reviendrons dessus plus tard)
- **Rapide** : Deploy en 2 secondes au lieu de 2 minutes
- **Safe** : Vous cassez rien sur le vrai AWS

Pour nous, ça améliore notre façon de développer. On peut tester directement l'appel à la lamda et non plus le code contenu dans la lamda (ca à sa nuance !).

### Installation avec Docker

Un simple `docker-compose.yml` suffit

```yaml
version: '3.8'

services:
  localstack:
    image: localstack/localstack:latest
    ports:
      - "4566:4566"  # Port principal LocalStack
    environment:
      - SERVICES=lambda,apigateway,s3,cloudformation,logs
      - DEBUG=1
      - LAMBDA_EXECUTOR=docker
      - AWS_DEFAULT_REGION=eu-west-1
    volumes:
      - "/var/run/docker.sock:/var/run/docker.sock"
```

Démarrez avec

#### Démarrage

```bash
docker compose up -d
```

LocalStack tourne maintenant sur `http://localhost:4566`. Pour déployer dessus au lieu d'AWS, on utilise les lignes de commande `awslocal` et `samlocal` qui sont en réalité des wrappers des commandes `aws` et `sam` mais qui pointent directement vers localstack.

### Installer les outils

```bash
pip install aws-sam-cli awscli-local
```

Ensuite, le workflow de dev devient trivial
```bash
# 1. Coder votre Lambda dans src/handlers/ et ajouter dans template.yaml

# 2. Build
samlocal build

# 3. Deploy sur LocalStack
samlocal deploy

# 4. Tester
awslocal lambda invoke \
    --function-name hello-world-function \
    response.json
    
cat response.json  # Voir le résultat
```

Des modifs à faire ? Modifier votre code, refaites `samlocal build && samlocal deploy`, c'est redéployé en quelques secondes. Et vous pouvez itérer rapidement

## Lambda Layers : Partager du code entre Lambdas

Au bout d'un moment, vous allez avoir plusieurs Lambdas. Et il se peut que ces lamdas partagent du code - des fonctions utilitaires, du formatage de réponses etc...

Le soucis, c'est que les lambdas sont idépendante. Si vous avez une besoin d'une fonction entre deux lambdas, vous devez la copier-coller dans chaque Lambda.

Enfin nous mentons, car **les Lambda Layers règlent ce problème.** Un Layer, c'est un package de code réutilisable que plusieurs Lambdas peuvent partager. 

Dans notre cas, on va créer un Layer avec nos fonctions de formatage de réponses, comme ça toutes nos Lambdas retournent le même format JSON.

### Structure d'un Layer

```
layers/
└── custom_utils/
    ├── __init__.py
    ├── display.py          # Vos fonctions
    └── requirements.txt    # Dépendances (optionnel)
```

**display.py** :
```python
import json

def format_response(status_code, data):
    """Formatte une réponse standard API Gateway"""
    return {
        "statusCode": status_code,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(data)
    }

def get_greeting(name):
    """Message de salutation personnalisé"""
    return f"Hello, {name}!"
```

Dans `template.yaml`, déclarez le Layer

```yaml
Resources:
  CustomUtilsLayer:
    Type: AWS::Serverless::LayerVersion
    Properties:
      LayerName: custom-utils-layer
      ContentUri: layers/custom_utils/
      CompatibleRuntimes:
        - python3.12

  HelloWorldFunction:
    Type: AWS::Serverless::Function
    Properties:
      CodeUri: src/handlers/hello_world/
      Handler: app.lambda_handler
      Layers:
        - !Ref CustomUtilsLayer  # Utilise le Layer
```

Dans votre Lambda, importez directement

```python
from custom_utils import format_response, get_greeting

def lambda_handler(event, context):
    name = event.get("queryStringParameters", {}).get("name", "World")
    greeting = get_greeting(name)
    return format_response(200, {"message": greeting})
```

Simple, élégant, réutilisable. Sauf que... **ça marche pas sur LocalStack** 😅

## Le Problème des Layers sur LocalStack

Sur AWS, quand vous utilisez un Layer, AWS le monte automatiquement dans `/opt/python` (si vous developez en python bien sur) et tout fonctionne. Sur LocalStack... non. Vous déployez, vous testez, et boom :

```
ModuleNotFoundError: No module named 'custom_utils'
```

LocalStack crée bien le Layer, il l'associe à votre Lambda, mais il ne le monte pas dans le container d'exécution. Pourquoi ? Car c'est une feature premium de LocalStack Pro.

**La solution ?** Un petit workaround Docker. Pas très élégant, mais ça fonctionne !

### Le Workaround : Monter les Layers manuellement

L'idée : dire à LocalStack de monter votre dossier `layers/` directement dans les containers Lambda via Docker volumes.

Modifiez votre `docker-compose.yml`

```yaml
services:
  localstack:
    image: localstack/localstack:latest
    ports:
      - "4566:4566"
    environment:
      - SERVICES=lambda,apigateway,s3,cloudformation,logs
      - DEBUG=1
      - LAMBDA_EXECUTOR=docker
      - LAMBDA_DOCKER_NETWORK=localstack-sam-network
      
      # 🔧 LE WORKAROUND : Monte les layers dans les containers Lambda
      - LAMBDA_DOCKER_FLAGS=-v /var/www/hackday/localstack-test/layers:/opt/python:ro
      
      - AWS_DEFAULT_REGION=eu-west-1
    volumes:
      - "/var/run/docker.sock:/var/run/docker.sock"
      
      # 🔧 LE WORKAROUND : Monte les layers dans LocalStack
      - "/var/www/hackday/localstack-test/layers:/opt/python:ro"
    networks:
      - localstack-sam-network

networks:
  localstack-sam-network:
    driver: bridge
```

**Important** : Remplacez `/var/www/hackday/localstack-test/layers` par le **chemin absolu** vers votre dossier layers.

### Comment ça marche ?

1. `LAMBDA_DOCKER_FLAGS` dit à LocalStack : "Quand tu crées un container Lambda, monte ce volume dedans"
2. Le volume monte votre dossier `layers/` dans `/opt/python` du container Lambda
3. Python peut maintenant importer depuis `/opt/python/custom_utils/`

### Les limitations du workaround

Soyons honnêtes, ce workaround a des défauts :

1. **Pas de versioning** : Tous les Lambdas utilisent la même version du Layer
2. **Pas ISO a AWS** : Sur AWS, la structure est différente. Après vous pouvez toujours payer.
3. **Pas de hot-reload** : Meme si vous avez un volume monté, LocalStack "crée" le package au moment du déploiement. Donc si vous modifiez le code du Layer, il faut redeployer la Lambda. La version premium de LocalStack permet peut-être le hot-reload, nous n'avons pas testé.

## Conclusion

Voilà comment on a setup notre environnement de dev Lambda. C'est pas parfait - le workaround des Layers est un hack - mais ça marche et ça nous fait gagner un temps fou.

**Le setup complet** :
1. LocalStack pour émuler AWS en local
2. SAM pour définir l'infrastructure
3. Un workaround Docker pour les Layers
4. Des Makefiles pour automatiser

**Ce qui change dans le quotidien** :
- Developement de bout en bout sur une feature en local
- Tests illimités sans voir la facture AWS exploser
- Tout le monde a le même environnement (docker-compose)

Pour notre use case (backend SQL + Hasura + Lambdas Python pour les traitements complexes), c'est le setup idéal. On garde Hasura pour les requêtes CRUD classiques, et on sort l'artillerie Lambda quand on a besoin de Python.

Si vous êtes dans une situation similaire, nous vous encourageons vraiment à tester LocalStack. Oui, il y a des petits hacks à faire (les Layers...), mais le gain en productivité est énorme.

Et mention spéciale à SAM qui rend la gestion de l'infrastructure super simple.