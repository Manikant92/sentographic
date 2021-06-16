from datetime import datetime, date, timedelta
from geopy.geocoders import Nominatim
from contrib import news_api
from contrib import expert_api
from contrib import visualization_functions
from contrib import twitter_functions
from contrib import dataframe_functions
from contrib import analysis_functions
from django.conf import settings
import requests
import numpy as np
import matplotlib.pyplot as plt
import base64
import io
import json
import re
import urllib
import ast
import pandas as pd
# Starting a Matplotlib GUI outside of the main thread will likely fail.
import matplotlib
matplotlib.use('Agg')


yesterday = date.today() - timedelta(days=30)
yesterday = yesterday.strftime('%Y-%m-%d')


def convert_plot_to_uri(plot):
    plt.imshow(plot, interpolation="bilinear")
    plt.tight_layout(pad=0)
    plt.axis("off")
    figure = plt.gcf()
    # Starting a Matplotlib GUI outside of the main thread will likely fail.
    plt.close()
    buffer = io.BytesIO()
    figure.savefig(buffer, format='png', dpi=100)
    # added as part of Starting a Matplotlib GUI outside of the main thread will likely fail.
    # figure.close()
    buffer.seek(0)
    string = base64.b64encode(buffer.read())
    return urllib.parse.quote(string)


def prepare_tweet_dataframe(search_query):
    print('Creating dataframe')
    twitter_dataframe = dataframe_functions.create_new_dataframe()
    # Need to add search query here
    twitter_json_data = twitter_functions.get_tweets_data(search_query)
    for data in twitter_json_data:
        twitter_dataframe = twitter_dataframe.append(dataframe_functions.get_dataframe_row_values(data),
                                                     ignore_index=True)
    print('Scraped Data from Twitter')
    twitter_dataframe = sort_twitter_dataframe(twitter_dataframe)
    print('Created initial Twitter Dataframe')
    twitter_dataframe = prepare_sentiment_dataframe(twitter_dataframe)
    twitter_dataframe.to_csv('#tweets.csv', index=False, encoding='utf-8')
    print('Created Sentiment Dataframe')
    return twitter_dataframe


def sort_twitter_dataframe(dataframe):
    return dataframe.sort_values(by='created_at', axis=0, ascending=True, inplace=False, kind='quicksort',
                                 na_position='last')


def prepare_sentiment_dataframe(twitter_dataframe):
    twitter_dataframe['sentiment'] = np.array(
        [dataframe_functions.analyze_sentiment(tweet) for tweet in twitter_dataframe['tweet_text']])
    # twitter_dataframe['subjectivity'] = np.array(
    #     [dataframe_functions.get_subjectivity(tweet) for tweet in twitter_dataframe['tweet_text']])
    # twitter_dataframe['polarity'] = np.array(
    #     [dataframe_functions.get_polarity(tweet) for tweet in twitter_dataframe['tweet_text']])
    return twitter_dataframe


def sentiment_analysis(twitter_dataframe):
    result_dict = {
        'sentiment': analysis_functions.get_sentiment(twitter_dataframe),
        'tweet_timeline_graph': visualization_functions.get_tweet_count_over_time_graph(twitter_dataframe),
        'weekly_breakdown': visualization_functions.get_weekly_breakdown(twitter_dataframe),
        'total_tweets': len(twitter_dataframe),
        'tweet_text_cloud': visualization_functions.get_wordcloud(twitter_dataframe),
        'tweet_screenname_cloud': visualization_functions.get_top_tweeters(twitter_dataframe),
        'tweet_location_map': visualization_functions.get_geomap(twitter_dataframe),
        'hashtag_cloud': visualization_functions.get_hashtag_cloud(twitter_dataframe),
        'tweet_source': analysis_functions.get_tweet_source_dict(twitter_dataframe),
        'total_favourites': twitter_dataframe['favourites_count'].sum(),
        'total_retweets': twitter_dataframe['retweet_count'].sum(),
        'total_reach': twitter_dataframe['followers_count'].sum(),
        'unique_users': twitter_dataframe['screenname'].nunique(),
        'sentiment_timeline': visualization_functions.get_sentiment_timeline(twitter_dataframe),
        'avg_sentiment': int(twitter_dataframe['sentiment'].sum()),
        'overall_sentiment': analysis_functions.get_overall_sentiment(int(twitter_dataframe['sentiment'].sum()))
    }
    return result_dict


def news_sentiment_analysis(news_dataframe):
    result_dict = {
        'sentiment': analysis_functions.get_sentiment(news_dataframe),
        'news_timeline_graph': visualization_functions.get_news_count_over_time_graph(news_dataframe),
        'weekly_breakdown': visualization_functions.get_weekly_breakdown(news_dataframe),
        'total_news': len(news_dataframe),
        'news_text_cloud': visualization_functions.get_news_wordcloud(news_dataframe),
        'news_author_cloud': visualization_functions.get_top_news_author(news_dataframe),
        # 'tweet_location_map': visualization_functions.get_geomap(news_dataframe),
        'entity_cloud': visualization_functions.get_entity_cloud(news_dataframe),
        'news_source': analysis_functions.get_tweet_source_dict(news_dataframe),
        'lemma_cloud': visualization_functions.get_mainlemma_cloud(news_dataframe),
        'unique_sources': news_dataframe['source'].nunique(),
        'unique_links': news_dataframe['url'].nunique(),
        'avg_sentiment': int(news_dataframe['sentiment'].sum()),
        'unique_authors': news_dataframe['author'].nunique(),
        'sentiment_timeline': visualization_functions.get_news_sentiment_timeline(news_dataframe),
        'overall_sentiment': analysis_functions.get_overall_sentiment(int(news_dataframe['sentiment'].sum()))}
    return result_dict


def deEmojify(text):
    regrex_pattern = re.compile(pattern="["u"\U0001F600-\U0001F64F"  # emoticons
                                        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                                        u"\U0001F680-\U0001F6FF"  # transport & map symbols
                                        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                                        "]+", flags=re.UNICODE)
    return regrex_pattern.sub(r'', text)


# def get_geocode(city):
#     coordinates = None
#     city = deEmojify(city)
#     query_object = {'key': settings.GOOGLE_MAPS_API_KEY, 'address': city}
#     try:
#         data = requests.get(settings.GOOGLE_GEOCODE_API_URL,
#                             params=query_object)
#         json_data = json.loads(data.text)
#         coordinates = (json_data['results'][0]['geometry']['location']['lat'],
#                        json_data['results'][0]['geometry']['location']['lng'])
#     except Exception as e:
#         print('Exception in Geocode: ', str(e))
#         print(f'Exception occurred while finding the geocode for {city}')
#     return coordinates


# address = 'New Hampshire USA'
def get_geocode(city):
    coordinates = None
    city = deEmojify(city)
    try:

        geolocator = Nominatim(user_agent="Your_Name")
        location = geolocator.geocode(city)
        # print(location.address)
        print((location.latitude, location.longitude))
        coordinates = (location.latitude, location.longitude)
    except:
        print(f'Exception occurred while finding the geocode for {city}')
    return coordinates


def get_geocode_city(city_list):
    coordinates_list = []
    for city in city_list:
        coordinates_list.append([city, get_geocode(city)])
    return coordinates_list


def prepare_search_query(hashtag_list, num_tweets=50, from_date=yesterday, language='en'):
    return {
        'hashtag_list': hashtag_list,
        'num_tweets': num_tweets,
        'from_date': from_date,
        'language': language
    }


def get_news_source_name(json):
    name = 'Undefined'
    try:
        if not isinstance(json, dict):
            json = ast.literal_eval(json)
        name = json['name']
    except:
        name = 'Undefined'
    return name


def modify_cols(df):
    df['content_exp'] = df['content'].apply(
        lambda x: expert_api.full_eda_news(x))
    # days = {0: 'Monday', 1: 'Tuesday', 2: 'Wednesday',
    #         3: 'Thursday', 4: 'Friday', 5: 'Saturday', 6: 'Sunday'}
    days = {0: 'Mon', 1: 'Tue', 2: 'Wed',
            3: 'Thu', 4: 'Fri', 5: 'Sat', 6: 'Sun'}
    df['source'] = df['source'].apply(lambda x: get_news_source_name(x))
    df['datetime'] = pd.to_datetime(df['datetime'])
    df['date'] = df['datetime'].dt.date
    df['time'] = df['datetime'].dt.time
    df['day'] = df['datetime'].dt.dayofweek
    df['day'] = df['day'].map(days)
    df[['lemma', 'entity', 'sentiment']] = pd.DataFrame(
        df.content_exp.tolist(), index=df.index)
    # df.to_csv('news_expert.csv', index=False)
    df.to_csv('news_expert.csv', index=False)
    return df


def prepare_news_content(search_query, num_articles):
    news_df = news_api.get_news_content(
        query=search_query, page_size=num_articles)
    news_df = modify_cols(news_df)
    analysis_res = news_sentiment_analysis(news_df)
    return analysis_res
