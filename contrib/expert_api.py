import os
from expertai.nlapi.cloud.client import ExpertAiClient
from expertai.nlapi.common.model import sentiment
from django.conf import settings

os.environ["EAI_USERNAME"] = settings.EAI_USERNAME
os.environ["EAI_PASSWORD"] = settings.EAI_PASSWORD
client = ExpertAiClient()


def get_sentiment(tweet_txt):
    try:
        language = 'en'
        document = client.specific_resource_analysis(
            body={"document": {"text": tweet_txt}},
            params={'language': language, 'resource': 'sentiment'})
        sentiment = document.sentiment.overall
        print("Output overall sentiment: ", sentiment)
        return sentiment
    except Exception as e:
        print("Exception due to: ", str(e))
        return 0


def full_eda_news(text):
    try:
        language = 'en'
        output = client.full_analysis(
            body={"document": {"text": text}}, params={'language': language})
        lemmas = []
        entities = []
        sentiments = []
        # categories = []
        for lemma in output.main_lemmas:
            lemmas.append(lemma.value)
        for entity in output.entities:
            entities.append(entity.lemma)
        # for sentiment in output.sentiment.items:
        sentiment = output.sentiment.overall
        # for category in output.categories:
        #     categories.append([category.namespace, category.label])
        return [lemmas, entities, sentiment]
    except Exception as e:
        print('Exception in Full EDA Analysis: ', str(e))
        return ['Undefined', 'Undefined', 'Undefined']
