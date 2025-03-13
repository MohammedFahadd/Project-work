import tweepy
import json

# Replace with your actual Bearer token
bearer_token = "AAAAAAAAAAAAAAAAAAAAAJ8kzgEAAAAASMRxJ0brUzRamE%2BlINyY%2BMO4CL0%3DNl3GO21YEX3xva5dLVASrYlEtZoJdwjP04Tgg22aNtRXz82PRB"

# Create a Tweepy client for Twitter API v2
client = tweepy.Client(bearer_token=bearer_token)

# Define your search query
query = "python -is:retweet"
tweet_count = 10

try:
    # Fetch recent tweets
    response = client.search_recent_tweets(
        query=query,
        max_results=tweet_count,
        tweet_fields=["created_at", "text", "author_id", "lang"]
    )

    # Write tweets to data.json
    if response.data:
        with open("data.json", "w", encoding="utf-8") as f:
            for tweet in response.data:
                tweet_dict = tweet.data
                f.write(json.dumps(tweet_dict, ensure_ascii=False) + "\n")
        print(f"Saved {len(response.data)} tweets to data.json.")
    else:
        print("No tweets returned.")

except tweepy.errors.TooManyRequests:
    print("Rate limit exceeded. Please wait before trying again.")
except tweepy.TweepyException as e:
    print(f"An error occurred: {e}")