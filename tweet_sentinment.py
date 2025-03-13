import sys
import json

def main():
    afinn_file = sys.argv[1]
    data_file = sys.argv[2]
    
    scores = {}
    with open(afinn_file, "r", encoding="utf-8") as f:
        for line in f:
            term, score = line.split("\t")
            scores[term] = int(score.strip())  
    
    with open(data_file, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:

                print(0)
                continue
            
            try:
                post = json.loads(line)
            except json.JSONDecodeError:
                print(0)
                continue
            
            text = ""
            if "text" in post:
                text = post["text"]
            elif "full_text" in post:
                text = post["full_text"]
            
            words = text.lower().split()
            sentiment_score = 0
            for word in words:

                sentiment_score += scores.get(word, 0)
            

            print(sentiment_score)

if __name__ == "__main__":
    main()