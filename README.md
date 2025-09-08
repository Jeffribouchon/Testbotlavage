# Agent IA de réservation - Déploiement rapide

## Pré-requis
- Docker & Docker Compose
- Compte Twilio (WhatsApp API)
- Clé API OpenAI
- Compte Google Cloud avec service account pour Calendar API

## Lancement
1. Copier `web/.env.example` vers `web/.env` et renseigner les clefs
2. Placer le fichier JSON du service account Google dans `web/app/credentials/google-service-account.json`
3. Build & run:

```bash
docker-compose up --build -d
```

4. Configure le webhook Twilio pour pointer sur `https://yourdomain.com/webhook/twilio`

## Tests NLP
Tu peux tester la brique NLP localement avec:

```bash
docker-compose run --rm web python app/nlp_client.py
```

Cela analysera une phrase de test et affichera le JSON extrait.

## Tests unitaires (NLP)
Crée un fichier `test_nlp.py` et ajoute :

```python
from app.nlp_client import NlpClient

def test_booking_message():
    client = NlpClient()
    msg = "Bonjour, je veux un lavage complet samedi à 10h"
    parsed = client.parse_message(msg)
    assert 'intent' in parsed
    assert parsed['intent'] in ['book','clarify']
```

Puis exécute :

```bash
docker-compose run --rm web pytest
```
