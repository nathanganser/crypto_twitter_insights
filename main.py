# import tweepy
import tweepy as tw
import os
from dotenv import load_dotenv
from helper import show_tweet, most_important_tweets, get_most_important_low_cap_coins, search_tweets_for_keywords, \
    get_ids_from_usernames, find_new_crypto_projects, find_financing_rounds, show_user, most_retweeted_tweets
from language_processing import ct_market_sentiment

load_dotenv()

# variables
my_api_key = os.environ['api_key']
my_api_secret = os.environ['key_secret']
twitter_accounts = ["kyled116", "DCLBlogger", "joeykrug", "tarunchitra", "econoar", "gpl_94", "n2ckchong", "QwQiao",
                    "kyled116", "zhusu", "gmoneyNFT", "seedphrase", "jonwu_", "QwQiao", "n2ckchong", "gpl_94",
                    "econoar", "tarunchitra", "scott_lew_is", "tomhschmidt", "FrankResearcher", "Arthur_0x",
                    "TheCryptoDog", "Beetcoin", "CL207", "Fjvdb7", "scupytrooples", "loomdart", "evabeylin",
                    "hedgedhog7", "devops199fan", "arjunblj", "UniHax0r", "charl3svii"]
twitter_account_ids = [1140429573978378241, 997715301545361408, 1098681096, 53836928, 14101591, 1196608843490480135,
                       1287487599691456512, 712457848874086400, 1140429573978378241, 79714172, 1311393885806100481,
                       3005650652, 15809138, 712457848874086400, 1287487599691456512, 1196608843490480135, 14101591,
                       53836928, 3226266525, 239090734, 1102925387472998401, 1357451976, 887748030304329728, 1389203360,
                       1073132650309726208, 1075413923908804608, 1012777913299689477, 2603525726, 342470910,
                       995167085666828288, 1256327425916616704, 25552514, 1269095159192485896, 316064087]

# authenticate
auth = tw.OAuthHandler(my_api_key, my_api_secret)
api = tw.API(auth, wait_on_rate_limit=True)

# gather the last 20 tweets from the influencer list
tweet_set = []
print('loading tweets...')

for account in twitter_account_ids:
    for tweet in tw.Cursor(api.user_timeline, id=account).items(100):
        tweet_set.append(tweet)

print(f'loaded {len(tweet_set)} tweets from {len(twitter_account_ids)} accounts')




def five_most_important_tweets_of_the_day(tweet_set):
    print('======= 5 important tweets of the day =========')
    five_most_important_tweets = most_important_tweets(tweet_set, tweets_returned=5)
    for t in five_most_important_tweets:
        show_tweet(t)
        print('---------')


def ten_important_coin_telegraph_articles(tweet_set):
    print('=======  10 important coin_telegraph_articles ========')
    tweets_with_article = search_tweets_for_keywords(tweet_set, ["cointelegraph.com"])
    if tweets_with_article:
        important_cointelegraph_tweets = most_important_tweets(tweets_with_article, twitter_account_ids, tweets_returned=10)
        if important_cointelegraph_tweets:
            for t in important_cointelegraph_tweets:
                show_tweet(t)
                print('---------')
    else:
        print('Could not find any coin_telegraph articles')


def most_important_low_cap_coins(tweet_set):
    result = get_most_important_low_cap_coins(tweet_set)
    print('=== Most talked about low market cap coins ===')
    print(result)

def new_crypto_project(tweet_set):
    print('==== New Crypto Projects =====')
    usernames = find_new_crypto_projects(tweet_set)
    for user in usernames:
        u = api.get_user(user)
        show_user(u)
        print('-----')

def recent_funding_rounds():
    tweets = find_financing_rounds()
    if tweets:
        print('====== New financing rounds ======')
        for t in tweets:
            show_tweet(t)
            print('---------')


five_most_important_tweets_of_the_day(tweet_set) # better with more tweets
most_retweeted_tweets(tweet_set)

ten_important_coin_telegraph_articles(tweet_set)
ct_market_sentiment(tweet_set)
new_crypto_project(tweet_set)
most_important_low_cap_coins(tweet_set)
recent_funding_rounds() # Only looks at ICO_Analytics
