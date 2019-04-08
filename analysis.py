import io
import json
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types
from google.oauth2 import service_account

def analyze(message, client):
    document = types.Document(content = message, type = enums.Document.Type.PLAIN_TEXT)
    sentiment = client.analyze_sentiment(document=document).document_sentiment
    print(str(sentiment.score))
    return sentiment
"""
# Need your own private GCP service account key for the api calls
with open('apikey.json', 'r') as key_file:
    key = key_file.read()
    key_json = json.loads(key, strict=False)
    creds = service_account.Credentials.from_service_account_info(key_json)

client = language.LanguageServiceClient(credentials=creds)

text = 'Fuck! I\'m so pissed. That movie was so bad I can\'t believe I spent money on that.'

sentiment = analyze(text)

print('Text: {}'.format(text))
print('Sentiment: {}, {}'.format(sentiment.score, sentiment.magnitude))
"""
