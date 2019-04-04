from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types

def analyze(message):
    document = types.Document(content = message, type = enums.Document.Type.PLAIN_TEXT)
    sentiment = client.analyze_sentiment(document=document).document_sentiment
    return sentiment



client = language.LanguageServiceClient()

text = 'Fuck! I\'m so pissed. That movie was so bad I can\'t believe I spent money on that.'

sentiment = analyze(text)

print('Text: {}'.format(text))
print('Sentiment: {}, {}'.format(sentiment.score, sentiment.magnitude))
