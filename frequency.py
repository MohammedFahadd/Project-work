import sys
import json

def main():
    tweet_file = sys.argv[1]

    term_counts = {}  
    total_terms = 0.0  

    with open(tweet_file, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                post = json.loads(line)
            except json.JSONDecodeError:
                continue
            text = post.get("text", "") or post.get("full_text", "")
            if not text:
                continue

            words = text.lower().split()

            for word in words:
                if word:  
                    term_counts[word] = term_counts.get(word, 0) + 1
                    total_terms += 1

    for term, count in term_counts.items():
        frequency = count / total_terms
        print(f"{term} {frequency}")

if __name__ == "__main__":
    main()