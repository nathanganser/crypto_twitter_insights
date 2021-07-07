# Crypto Twitter Insights
### Strategy to gather insights from Twitter
1. Instead of searching throughout the whole of Twitter, we focus on a specific set of `influencers` which we trust to have valuable insights.
2. Abstract functions are used and reused to: sort tweets by importance, search for keywords/links/accounts, ...
3. Sets of tweets from those influencers are aggregated to answer the questions below.



*Info: Depending on the set of tweets used, one can search through a day, week or month.*

## 5 Most Important Tweets of the Day/Week/Month
*A function that takes a set of tweets and looks at the count of likes & retweets + how many influencers retweeted/liked to rank them.*

## 5 Most Important Cointelegraph Articles of the Day (& Top 5 Week)
*A function that searches for cointelegraph.com links in a tweetset and then feeds this filtered set to the above function.*

## 5 Most Important Non-Cointelegraph Articles of the Day (& Top 5 Week)
TODO *A function that searches for x,y,z links in a tweet set and then runs this set through the importance algorithm.*

## 5 Most Discussed LowMarketCap Cryptocurrencies of the Day (& Week)
*A function that gets LowMarketCap coins from Coinmarketcap and searches for their names & tickers in a tweet set.*

## CT Market Sentiment
*Using nltk to do a sentiment analysis on a set of tweets*

## List of New Projects
*Searching for twitter accounts in a set of tweets that have been created in 2021 and have less than 500 followers.*

## List of Daily Financing Rounds
*Looking at @ICO_Analytics's tweets and filter for specific keywords*

### Improvements for production
-[ ] Build API
-[ ] Reduce need to call Twitter api to avoid hitting rate limit errors

