# from expertai.nlapi.cloud.client import ExpertAiClient
# from matplotlib.pyplot import title
from newsapi import NewsApiClient
# from numpy.core.numeric import full
import pandas as pd
# import ast
from datetime import datetime, date, timedelta
from django.conf import settings
# from contrib import helper_functions

# Init
newsapi = NewsApiClient(api_key=settings.NEWSAPI_KEY)
yesterday = date.today() - timedelta(days=2)
yesterday = yesterday.strftime('%Y-%m-%d')
today = datetime.today().strftime('%Y-%m-%d')


def get_news_content(query, page_size=50):
    # query = str()
    query = ''.join(query)
    all_articles = newsapi.get_everything(q=query, qintitle=query, from_param=yesterday,
                                          to=today, language='en', sort_by='popularity', page_size=page_size, page=1)
    content = []
    title = []
    sources = []
    authors = []
    urls = []
    datetimes = []
    for res in all_articles['articles']:
        content.append(res['content'])
        sources.append(res['source'])
        authors.append(res['author'])
        urls.append(res['url'])
        datetimes.append(res['publishedAt'])
        title.append(res['title'])
    df = pd.DataFrame({'title': title, 'content': content, 'source': sources,
                       'author': authors, 'url': urls, 'datetime': datetimes})
    return df
