import nltk
from nltk.sentiment import SentimentIntensityAnalyzer

sia = SentimentIntensityAnalyzer()


#nltk.download([
#    "names",
#    "stopwords",
#    "state_union",
#    "twitter_samples",
#    "movie_reviews",
#    "averaged_perceptron_tagger",
#    "vader_lexicon",
#    "punkt",
# ])

def ct_market_sentiment(tweet_set):
    neg, neu, pos, compound = 0, 0, 0, 0
    for tweet in tweet_set:
        scores = sia.polarity_scores(tweet.text)
        neg += scores['neg']
        neu += scores['neu']
        pos += scores['pos']
        compound += scores['compound']
        #print(f"neg: {scores['neg']}, neu: {scores['neu']}, pos: {scores['pos']}, compound: {scores['compound']}")
        #print(tweet.text)
        #print('------------')
    print('==== Market Sentiment =====')

    print(f'Negative: {neg}, Neutral: {neu}, Positive: {pos}, Compound: {compound}')
    return neg, neu, pos
