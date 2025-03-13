import sys
import json

def main():
    afinn_file = sys.argv[1]     
    tweet_file = sys.argv[2]    

    scores = {}
    with open(afinn_file, "r", encoding="utf-8") as f:
        for line in f:
            term, score = line.split("\t")
            scores[term] = int(score.strip())

    unknown_word_sentiment = {}
    unknown_word_count = {}

    with open(tweet_file, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            
            try:
                tweet_data = json.loads(line)
            except json.JSONDecodeError:
                continue
            text = tweet_data.get("text", "") or tweet_data.get("full_text", "")
            if not text:
                continue

            words = text.lower().split()
            tweet_sentiment = 0
            for word in words:
                tweet_sentiment += scores.get(word, 0)

            for word in words:
                if word not in scores: 
                    if word not in unknown_word_sentiment:
                        unknown_word_sentiment[word] = 0.0
                        unknown_word_count[word] = 0
                    unknown_word_sentiment[word] += tweet_sentiment
                    unknown_word_count[word] += 1

    for word in unknown_word_sentiment:
        avg_sentiment = unknown_word_sentiment[word] / unknown_word_count[word]
        print(f"{word} {avg_sentiment}")

if __name__ == "__main__":
    main()