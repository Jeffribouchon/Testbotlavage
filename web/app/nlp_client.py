import os
import openai
import json
from typing import Dict

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
OPENAI_MODEL = os.getenv('OPENAI_MODEL', 'gpt-4o')

openai.api_key = OPENAI_API_KEY

SYSTEM_PROMPT = (
    "Tu es un assistant spécialisé dans l'extraction d'intentions et d'entités pour un service de réservation de lavage automobile. "
    "Tu dois renvoyer strictement un JSON (sans texte additionnel) avec les champs suivants quand cela est pertinent:\n"
    "- intent: 'book'|'cancel'|'reschedule'|'clarify'\n"
    "- service: string (ex: 'lavage complet')\n"
    "- datetime: ISO8601 datetime string en Europe/Paris si fournie (ex: '2025-09-13T10:00:00')\n"
    "- duration_minutes: integer (durée estimée en minutes)\n"
    "- missing: boolean (true si des informations manquent)\n"
    "- missing_question: string (question à poser au client si des infos manquent)\n"
    "Si des informations sont manquantes, renvoie missing:true et missing_question. Sinon renvoie les champs intent/service/datetime/duration_minutes."
)

class NlpClient:
    def __init__(self, api_key=None, model=None):
        self.api_key = api_key or OPENAI_API_KEY
        self.model = model or OPENAI_MODEL

    def parse_message(self, text: str) -> Dict:
        prompt = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"Analyse ce message et renvoie le JSON: {text}"}
        ]

        try:
            resp = openai.ChatCompletion.create(
                model=self.model,
                messages=prompt,
                temperature=0.0,
                max_tokens=400,
            )
        except Exception:
            return {"intent": "clarify", "missing": True, "missing_question": "Quel service et quelle date souhaitez-vous ?"}

        content = resp['choices'][0]['message']['content'].strip()

        try:
            start = content.find('{')
            end = content.rfind('}')
            if start != -1 and end != -1:
                json_text = content[start:end+1]
            else:
                json_text = content
            parsed = json.loads(json_text)
        except Exception:
            return {"intent": "clarify", "missing": True, "missing_question": "Quel service (intérieur/extérieur/complet) et quelle date/heure souhaitez-vous ?"}

        return parsed

# Petit test local
if __name__ == '__main__':
    client = NlpClient()
    print(client.parse_message("Je veux un lavage complet demain à 14h"))
