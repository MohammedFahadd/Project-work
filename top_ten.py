import sys
import json

def main():
    tweet_file = sys.argv[1]

    hashtag_counts = {}

    with open(tweet_file, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            try:
                tweet = json.loads(line)
            except json.JSONDecodeError:
                continue

            entities = tweet.get("entities", {})
            hashtags = entities.get("hashtags", [])

            for h in hashtags:
                hashtag_text = h.get("text", "").lower()
                if hashtag_text:
                    hashtag_counts[hashtag_text] = hashtag_counts.get(hashtag_text, 0) + 1

    sorted_hashtags = sorted(hashtag_counts.items(), key=lambda x: x[1], reverse=True)

 
    top_10 = sorted_hashtags[:10]

    for hashtag, count in top_10:
        print(f"{hashtag} {count}")

if __name__ == "__main__":
    main()