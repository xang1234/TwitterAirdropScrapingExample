import json
import string
from collections import defaultdict
from snscrape.modules.twitter import Tweet

FILES = {
    "W": "data/word_frequencies.txt",
    "TA": "data/tweet_author_frequencies.txt",
    "H": "data/hashtag_frequencies.txt",
    "UM": "data/username_mention_frequencies.txt"
}
VALID_CHAR = set([char for char in list(string.ascii_lowercase + string.digits + "#@$-_'\"")])

def isValidWord(strippedWord: str) -> str:
    strippedWord = strippedWord.lower().strip().strip(" \n,.?!:;\"'")
    if strippedWord.isspace() or len(strippedWord) <= 2: return None
    if any(word in ignoredWords for word in (strippedWord, f"#{strippedWord}", f"${strippedWord}")): return None
    if any(char not in VALID_CHAR for char in strippedWord): return None
    return strippedWord

def writeDataToFile(data: dict, filepath: str) -> None:
    sortedData: list[tuple[str, int]] = sorted(data.items(), key = lambda kv: kv[1], reverse=True)
    maxCountDigits: int = len(str(sortedData[0][1])) # NOTE: Helps with lining up output for easy reading
    for contentCountTuple in sortedData:
        content: str = contentCountTuple[0]
        count: int = contentCountTuple[1]
        padding: str = " " * (maxCountDigits - len(str(count))) 
        filepath.write(f"{count}{padding} | {content}\n")

with open('tweets/aggregated_tweets.json', 'r', encoding='utf-8') as tweetsJsonLinesFile:
    allTweets: list[Tweet] = [Tweet(**{k: v for k, v in json.loads(line).items() if k != '_type'}) for line in tweetsJsonLinesFile]
    
with open('ignored_words.txt', 'r') as ignoredWordsFile:
    ignoredWords = set(list(word.lower().strip() for word in ignoredWordsFile.readlines()))

with (
    open(FILES["W"], 'w', encoding="utf-8") as WORDS_OUTFILE,
    open(FILES["TA"], 'w', encoding="utf-8") as TWEET_AUTHOR_OUTFILE,
    open(FILES["H"], 'w', encoding="utf-8") as HASHTAG_OUTFILE,
    open(FILES["UM"], 'w', encoding="utf-8") as USERNAME_MENTION_OUTFILE
):  
    wordFrequencies: dict = defaultdict(int)
    tweetAuthorFrequencies: dict = defaultdict(int)
    hashtagFrequencies: dict = defaultdict(int)
    usernameMentionFrequencies: dict = defaultdict(int)

    for tweet in allTweets:
        for word in tweet.content.strip().split():
            validWord = isValidWord(word)
            if validWord:
                wordFrequencies[validWord] += 1

        tweetAuthorFrequencies[f"@{tweet.user['username']} ({tweet.user['id']})"] += 1

        if tweet.hashtags:
            for hashtag in tweet.hashtags:
                hashtagFrequencies[f"#{hashtag}"] += 1
            
        if tweet.mentionedUsers:
            for user in tweet.mentionedUsers:
                usernameMentionFrequencies[f"@{user['username']}"] += 1

    writeDataToFile(wordFrequencies, WORDS_OUTFILE)
    writeDataToFile(tweetAuthorFrequencies, TWEET_AUTHOR_OUTFILE)
    writeDataToFile(hashtagFrequencies, HASHTAG_OUTFILE)
    writeDataToFile(usernameMentionFrequencies, USERNAME_MENTION_OUTFILE)
