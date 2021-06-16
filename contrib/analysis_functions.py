

def get_sentiment(dataframe):
    print('Analysing sentiments')
    sentiment_dict = {
        'Neutral': len(dataframe[dataframe['sentiment'] == 0]),
        'Weakly_Positive': len(dataframe[(dataframe['sentiment'] > 0) & (dataframe['sentiment'] <= 30)]),
        'Positive': len(dataframe[(dataframe['sentiment'] > 30) & (dataframe['sentiment'] <= 60)]),
        'Strongly_Positive': len(dataframe[(dataframe['sentiment'] > 60) & (dataframe['sentiment'] <= 100)]),
        'Weakly_Negative': len(dataframe[(dataframe['sentiment'] > -30) & (dataframe['sentiment'] < 0)]),
        'Negative': len(dataframe[(dataframe['sentiment'] > -60) & (dataframe['sentiment'] <= -30)]),
        'Strongly_Negative': len(dataframe[(dataframe['sentiment'] >= -100) & (dataframe['sentiment'] <= -60)])
    }
    print('Sentiment analysis Done')
    return sentiment_dict


def get_overall_sentiment(val):
    if val == 0:
        return 'Neutral'
    elif val > 0 and val <= 30:
        return 'Weakly Positive'
    elif val > 30 and val <= 60:
        return 'Positive'
    elif val > 60 and val <= 100:
        return 'Strongly Positive'
    elif val > -30 and val < 0:
        return 'Weakly Negative'
    elif val > -60 and val <= -30:
        return 'Negative'
    elif val > -100 and val <= -60:
        return 'Strongly Negative'


def get_tweet_source_dict(dataframe):
    source_dict = {}
    source = dict(dataframe['source'].value_counts())
    # Order source by descending order and return the top 6 sources
    sorted_dict = sorted(source.items(), key=lambda x: x[1], reverse=True)[0:6]
    for source, value in sorted_dict:
        source_dict[source] = value
    return source_dict
