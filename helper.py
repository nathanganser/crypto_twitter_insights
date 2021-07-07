import tweepy as tw
import webbrowser
from dotenv import load_dotenv
import os
from models import Tweet
import datetime
from coinmarketcap import get_low_market_cap_coins

load_dotenv()
my_api_key = os.environ['api_key']
my_api_secret = os.environ['key_secret']
auth = tw.OAuthHandler(my_api_key, my_api_secret)
api = tw.API(auth, wait_on_rate_limit=True)


def get_ids_from_usernames(usernames):
    ids = []
    for username in usernames:
        user = api.get_user(username)
        ids.append(user.id)
    print(ids)
    return ids


def show_tweet(tweet):
    print(f'Tweeted at {tweet.created_at} by {tweet.user.screen_name}. id: {tweet.id}')
    print(f'Text: {tweet.text}')
    print(f'Likes: {tweet.favorite_count}, Retweets: {tweet.retweet_count}')
    webbrowser.open("https://twitter.com/i/web/status/" + str(tweet.id))



def show_user(user):
    print(f'Name: {user.name} (location: {user.location}')
    print(f'Followers: {user.followers_count}, Description: {user.description}')
    print(f'Link: {user.url}')


def count_retweets_by_influencers(tweet_id, influencer_ids):
    # getting ids
    retweeters = api.retweeters(tweet_id)
    # print(f'got the retweets of that tweet: {retweeters}')
    return len(set(influencer_ids).intersection(retweeters))


def get_tweet_importance(tweet, retweet_weight=0.5, like_weight=0.3,
                         follower_weight=0.01, link_weight=10):
    tweet_importance = tweet.retweet_count * retweet_weight + tweet.favorite_count * like_weight + tweet.user.followers_count * follower_weight
    if "https" in tweet.text:
        tweet_importance += link_weight
    return tweet_importance


def most_important_tweets(tweet_set, tweets_returned=5):
    if not len(tweet_set) >= tweets_returned:
        return None

    important_tweets = tweet_set[0:tweets_returned]
    for tweet in tweet_set[0:]:
        # print(f'Looking at tweet: {tweet.text}')
        tweet_importance = get_tweet_importance(tweet)
        for i in range(0, len(important_tweets), +1):
            selected_tweet = important_tweets[i]
            selected_tweet_importance = get_tweet_importance(selected_tweet)
            if tweet_importance > selected_tweet_importance:
                important_tweets[i] = tweet
                break
    return important_tweets


def search_tweets_for_keywords(tweets, keywords):
    tweet_list = []
    for tweet in tweets:
        for keyword in keywords:
            if keyword in tweet.text.lower():
                tweet_list.append(tweet)
                break
    return tweet_list




def count_keywords_in_tweets(tweets, keywords):
    tweet_list = {}

    for keyword in keywords:
        tweet_list[keyword.lower()] = 0
    for tweet in tweets:
        for keyword in keywords:
            if keyword.lower() in tweet.text.lower():
                tweet_list[keyword.lower()] += 1
    important_coins = {}
    for el in tweet_list:
        if tweet_list.get(el) > 0:
            important_coins[el] = tweet_list.get(el)
    return important_coins


def get_most_important_low_cap_coins(tweets):
    coin_names = get_low_market_cap_coins()
    result = count_keywords_in_tweets(tweets, coin_names)
    return result


def search_links_in_tweets(tweets, link):
    link_tweets = []
    search_query = link
    for tweet in tweets:
        if tweet._json.get('entities').get('urls'):
            if search_query in tweet._json.get('entities').get('urls')[0].get('expanded_url'):
                link_tweets.append(tweet)
    if link_tweets:
        return link_tweets
    else:
        return None


# @decentraland @Uniswap @AudiusProject @all_smilesss @_jamiis @crispylines
def is_new_crypto_project(id):
    user = api.get_user(id)
    created_at = user.created_at
    six_months_ago = datetime.datetime.now() - datetime.timedelta(days=30 * 6)
    if created_at > six_months_ago:
        new_account = True
    else:
        new_account = False
    followers_count = user.followers_count
    # print(followers_count, new_account)
    return new_account and followers_count < 500


def find_new_crypto_projects(tweet_set):
    new_crypto_projects = []
    checked_accounts = []
    for tweet in tweet_set:
        for user in tweet.entities.get('user_mentions'):
            if user not in checked_accounts:
                checked_accounts.append(user)
                if is_new_crypto_project(user.get('screen_name')) and user.get(
                        'screen_name') not in new_crypto_projects:
                    new_crypto_projects.append(user.get('screen_name'))
    return new_crypto_projects


def find_financing_rounds():
    tweet_set = []
    for tweet in tw.Cursor(api.user_timeline, id="ICO_Analytics").items(100):
        tweet_set.append(tweet)
    keywords = ["investment lead", "public sale", "token sale", "raised", "the close of", "funding round",
                "been committed"]
    relevant_tweets = search_tweets_for_keywords(tweet_set, keywords)
    return relevant_tweets


def add_to_array(array, Tweet):
    for el in array:
        # print(f'comparing {el.id} and {Tweet.id}')
        if Tweet.id == el.id:
            # print(f'Already there, +1 count')
            el.retweet_count += 1
            el.retweeters += Tweet.retweeters
            return array
    array.append(Tweet)
    # print(f'added {Tweet.id} to the array, array length {len(array)}')
    return array


def most_retweeted_tweets(tweet_set):
    print(f'===== Most retweeted tweets ======')
    array = []
    for tweet in tweet_set:
        try:
            if tweet.retweeted_status:

                try:
                    if tweet.retweeted_status.quoted_status_id:
                        # print(f'2-retweet: {tweet.retweeted_status.quoted_status_id}, retweeted by: {tweet.id}')
                        t = Tweet(tweet.retweeted_status.quoted_status_id, tweet.id)
                        array = add_to_array(array, t)
                except Exception as e:
                    # print(f'1-retweet: {tweet.retweeted_status.id}, retweeted by: {tweet.id}')
                    t = Tweet(tweet.retweeted_status.id, tweet.id)
                    array = add_to_array(array, t)
                    pass
        except Exception as e:
            pass
    for el in array:
        if el.retweet_count > 2:
            print(f'Tweet id {el.id} was retweeted {el.retweet_count} times by {el.retweeters}')
