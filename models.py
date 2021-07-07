class CryptoProject:
    def __init__(self):
        self.name = None
        self.ticker = None
        self.website = None
        self.twitter_mentions = None  # in_past_7_days
        self.volume = None  # in_past_7_days
        self.backlinks = None  # total


class Tweet:
    def __init__(self, id, initial_retweet_id):
        self.id = id,
        self.retweeters = [initial_retweet_id],
        self.retweet_count = 1
