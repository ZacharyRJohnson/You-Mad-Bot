from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types

class Sentiment():
    """
        Simple class to hold data for calculated sentiment information from a collection
        of messages. Data such as average score/magnitude, max/min score from a collection, etc.
    """

    def __init__(self, avg_score, avg_mag):
        self.avg_score = avg_score
        self.avg_magnitude = avg_mag


def analyze(message, client):
    document = types.Document(content = message, type = enums.Document.Type.PLAIN_TEXT)
    sentiment = client.analyze_sentiment(document=document).document_sentiment
    return sentiment

def get_average_sentiment(messages, client):
    avg_score = 0
    avg_magnitude = 0
    counted_msgs = 0
    for msg in messages:
        sentiment = analyze(msg, client)
        score = sentiment.score
        magnitude = sentiment.magnitude
        
        '''
        Rarely does a document equal zero. More than likely the analysis couldn't accurately 
        be calculated for some reason so those messages will be left out of the average.
        '''
        if(score == 0.0):
            continue
        else:
            avg_score += score
            avg_magnitude += magnitude
            counted_msgs += 1
    avg_score = avg_score / counted_msgs
    avg_magnitude = avg_magnitude / counted_msgs

    return Sentiment(avg_score, avg_magnitude)
