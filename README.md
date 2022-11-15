Twitter: @NeetNort<br>
One off example I made for fun to test an idea... use it for reference if you'd like.<br>
ParseTweets.py is a quickly built 'Iteration 1' from the list below.<br>
Please note that the ignored_words.txt file is thrown together quickly, is very incomplete, and likely outright ignores viable candidate words.<br> 
Please also note that the file 'airdrop_tweets.json' was > 100mb and I am far too lazy to setup Git LFS for this. You'll have to run the command below and generate your own.

# Run snscrape command:
    snscrape --jsonl --progress --max-results 50000 twitter-search "airdrop since:2022-10-01 until:2022-11-14" > airdrop_tweets.json

# Pre-requisites
    1. Install python
    2. Run: >>> pip install snscrape
    3. Run: >>> snscrape --jsonl --progress --max-results 50000 twitter-search "airdrop since:2022-10-01 until:2022-11-14" > airdrop_tweets.json
    4. ... Wait for the above to finish (you can make a subprocess and batch the work - just run the commands from multiple terminals with different date ranges)
    5. Once the above is done, use one of the following options (increasing difficulty with diminishing time/value)

# Iteration 1: Naive - Raw word frequencies
    1. Scrape tweets that contain the word 'airdrop'
    2. Aggregate all words from all tweets found into object / file / database / etc.
    3. Remove all words that are obvious nonsense:
        a. Make an 'ignore' list: top 1,000+ english words, obvious words like ('bitcoin', 'crypto', 'airdrop', 'wallets'), etc.
        b. Filter out words that are 1-2 letters long, whitespace, emojis, or contain non-ascii/alphanumeric characters
    4. Make a collections.Counter of all words that survived the above filtering
    5. Return the most_common(N: int) words - if your wordlist & filters are not shit, most of these top results are already useful

# Iteration 2: Less Naive - Weighted words based on location relative to word 'airdrop' (and all of the above)
    1. Strong-bias for words in tweets that come directly before/after the word 'airdrop'
    2. Slight-bias for words that start with '#' or '@' and occur frequently or directly before/after the word 'airdrop'

# Iteration 3: Least Naive - Time-aware context, tweet velocity & sentiment analysis (and all of the above)
    1. Bias toward tweet velocity (i.e., tweets that start coming in rapidly with the same words are biased greatly)
    2. Parse dates found in tweet content and sort two results sets:
        a. Tweets with dates CLOSEST to current date
        b. Tweets with dates FURTHEST from current date
    3. NLP + sentiment analysis on tweet content
