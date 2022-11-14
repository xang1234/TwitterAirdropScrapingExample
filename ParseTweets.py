import json, string, collections, pprint

with open('50000_airdrop_tweets_since_20221001.json', 'r', encoding='utf-8') as tweetsJsonLinesFile:
    allJson = {i: json.loads(line) for i, line in enumerate(tweetsJsonLinesFile)}

with open('ignored_words.txt', 'r') as ignoredWordsFile:
    ignoredWords = set(list(word.lower().strip() for word in ignoredWordsFile.readlines()))

VALID_CHAR = set([char for char in list(string.ascii_lowercase + string.digits + "#@$-_'\"")])
def isValidWord(strippedWord: str) -> str:
    strippedWord = strippedWord.lower().strip().strip(" \n,.?!:;\"'")
    if strippedWord.isspace() or len(strippedWord) <= 2: return None
    if any(word in ignoredWords for word in (strippedWord, f"#{strippedWord}", f"${strippedWord}")): return None
    if any(char not in VALID_CHAR for char in strippedWord): return None
    return strippedWord

validWords = collections.Counter([validWord for tweet in allJson.values() for word in tweet['content'].strip().split() if (validWord := isValidWord(word))])
pprint.pprint(validWords.most_common(500))
