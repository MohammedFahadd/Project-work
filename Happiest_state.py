import sys
import json

us_state_abbrev = {
    'AL': 'Alabama',
    'AK': 'Alaska',
    'AZ': 'Arizona',
    'AR': 'Arkansas',
    'CA': 'California',
    'CO': 'Colorado',
    'CT': 'Connecticut',
    'DE': 'Delaware',
    'FL': 'Florida',
    'GA': 'Georgia',
    'HI': 'Hawaii',
    'ID': 'Idaho',
    'IL': 'Illinois',
    'IN': 'Indiana',
    'IA': 'Iowa',
    'KS': 'Kansas',
    'KY': 'Kentucky',
    'LA': 'Louisiana',
    'ME': 'Maine',
    'MD': 'Maryland',
    'MA': 'Massachusetts',
    'MI': 'Michigan',
    'MN': 'Minnesota',
    'MS': 'Mississippi',
    'MO': 'Missouri',
    'MT': 'Montana',
    'NE': 'Nebraska',
    'NV': 'Nevada',
    'NH': 'New Hampshire',
    'NJ': 'New Jersey',
    'NM': 'New Mexico',
    'NY': 'New York',
    'NC': 'North Carolina',
    'ND': 'North Dakota',
    'OH': 'Ohio',
    'OK': 'Oklahoma',
    'OR': 'Oregon',
    'PA': 'Pennsylvania',
    'RI': 'Rhode Island',
    'SC': 'South Carolina',
    'SD': 'South Dakota',
    'TN': 'Tennessee',
    'TX': 'Texas',
    'UT': 'Utah',
    'VT': 'Vermont',
    'VA': 'Virginia',
    'WA': 'Washington',
    'WV': 'West Virginia',
    'WI': 'Wisconsin',
    'WY': 'Wyoming'
}

def get_state_from_tweet(tweet):
    user_info = tweet.get("user", {})
    location = user_info.get("location", "")
    if not location:
        return None

    loc_up = location.upper()

    if "CALIFORNIA" in loc_up:
        return "CA"
    if "NEW YORK" in loc_up:
        return "NY"
    if "FLORIDA" in loc_up:
        return "FL"

    for abbr in us_state_abbrev:
        if f" {abbr} " in f" {loc_up} " or loc_up.endswith(f" {abbr}") or loc_up.startswith(f"{abbr} "):
            return abbr

    for abbr, full_name in us_state_abbrev.items():
        if full_name.upper() in loc_up:
            return abbr

    return None

def main():
    afinn_file_path = sys.argv[1]
    tweet_file_path = sys.argv[2]

    afinn_scores = {}
    with open(afinn_file_path, "r", encoding="utf-8") as af:
        for line in af:
            term, score = line.split("\t")
            afinn_scores[term] = int(score.strip())

    state_sentiment_sum = {}
    state_tweet_count = {}
    with open(tweet_file_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                tweet = json.loads(line)
            except json.JSONDecodeError:
                continue

            text = tweet.get("text", "") or tweet.get("full_text", "")
            if not text:
                continue

            words = text.lower().split()
            tweet_sentiment = sum(afinn_scores.get(w, 0) for w in words)

            state_abbr = get_state_from_tweet(tweet)
            if state_abbr:
                state_sentiment_sum[state_abbr] = state_sentiment_sum.get(state_abbr, 0) + tweet_sentiment
                state_tweet_count[state_abbr] = state_tweet_count.get(state_abbr, 0) + 1

    happiest_state = None
    happiest_avg = float("-inf")

    for abbr, total_sent in state_sentiment_sum.items():
        avg_sent = total_sent / state_tweet_count[abbr]
        if avg_sent > happiest_avg:
            happiest_avg = avg_sent
            happiest_state = abbr

    if happiest_state:
        print(happiest_state)
    else:
        print("No state found")

if __name__ == "__main__":
    main()
