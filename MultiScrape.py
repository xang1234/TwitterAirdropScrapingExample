"""
Parallelized extension of iteration 1
# NOTE: snscrape --jsonl --progress --max-results 50000 twitter-search "airdrop since:2022-10-01 until:2022-11-14" > airdrop_tweets.json
"""
from dataclasses import dataclass
import subprocess
import time

@dataclass
class Process:
    query: str
    since: str
    until: str
    max_results: int
    outfile_location: str
    progress: bool = False

    snscrape_module: str = "snscrape"
    jsonl_arg: str = "--jsonl"
    progress_arg: str = "--progress"
    max_results_arg: str = "--max-results"
    twitter_search_arg: str = "twitter-search"
    file_pipe: str = ">"

    def getProcessArgs(self):
        _args = [self.snscrape_module, self.jsonl_arg]
        if self.progress:
            _args.append(self.progress_arg)
        if self.max_results:
            _args.append(self.max_results_arg)
            _args.append(str(self.max_results))
        _args += [self.twitter_search_arg, f'"{self.query} {self.since} {self.until}"', self.file_pipe, self.outfile_location]
        return _args

def scrape():
    DAYS_LIST = [
        ("since:2022-09-01", "until:2022-09-02"),
        ("since:2022-09-02", "until:2022-09-03"),
        ("since:2022-09-03", "until:2022-09-04"),
        ("since:2022-09-04", "until:2022-09-05"),
        ("since:2022-09-05", "until:2022-09-06"),
        ("since:2022-09-06", "until:2022-09-07"),
        ("since:2022-09-07", "until:2022-09-08"),
        ("since:2022-09-08", "until:2022-09-09"),
        ("since:2022-09-09", "until:2022-09-10"),
        ("since:2022-09-10", "until:2022-09-11"),
        ("since:2022-09-11", "until:2022-09-12"),
        ("since:2022-09-12", "until:2022-09-13"),
        ("since:2022-09-13", "until:2022-09-14"),
        ("since:2022-09-14", "until:2022-09-15"),
        ("since:2022-09-15", "until:2022-09-16"),
        ("since:2022-09-16", "until:2022-09-17"),
        ("since:2022-09-17", "until:2022-09-18"),
        ("since:2022-09-18", "until:2022-09-19"),
        ("since:2022-09-19", "until:2022-09-20"),
        ("since:2022-09-20", "until:2022-09-21"),
        ("since:2022-09-21", "until:2022-09-22"),
        ("since:2022-09-22", "until:2022-09-23"),
        ("since:2022-09-23", "until:2022-09-24"),
        ("since:2022-09-24", "until:2022-09-25"),
        ("since:2022-09-25", "until:2022-09-26"),
        ("since:2022-09-26", "until:2022-09-27"),
        ("since:2022-09-27", "until:2022-09-28"),
        ("since:2022-09-28", "until:2022-09-29"),
        ("since:2022-09-29", "until:2022-09-30"),
        ("since:2022-09-30", "until:2022-10-01"),
        ("since:2022-10-01", "until:2022-10-02"),
        ("since:2022-10-02", "until:2022-10-03"),
        ("since:2022-10-03", "until:2022-10-04"),
        ("since:2022-10-04", "until:2022-10-05"),
        ("since:2022-10-05", "until:2022-10-06"),
        ("since:2022-10-06", "until:2022-10-07"),
        ("since:2022-10-07", "until:2022-10-08"),
        ("since:2022-10-08", "until:2022-10-09"),
        ("since:2022-10-09", "until:2022-10-10"),
        ("since:2022-10-10", "until:2022-10-11"),
        ("since:2022-10-11", "until:2022-10-12"),
        ("since:2022-10-12", "until:2022-10-13"),
        ("since:2022-10-13", "until:2022-10-14"),
        ("since:2022-10-14", "until:2022-10-15"),
        ("since:2022-10-15", "until:2022-10-16"),
        ("since:2022-10-16", "until:2022-10-17"),
        ("since:2022-10-17", "until:2022-10-18"),
        ("since:2022-10-18", "until:2022-10-19"),
        ("since:2022-10-19", "until:2022-10-20"),
        ("since:2022-10-20", "until:2022-10-21"),
        ("since:2022-10-21", "until:2022-10-22"),
        ("since:2022-10-22", "until:2022-10-23"),
        ("since:2022-10-23", "until:2022-10-24"),
        ("since:2022-10-24", "until:2022-10-25"),
        ("since:2022-10-25", "until:2022-10-26"),
        ("since:2022-10-26", "until:2022-10-27"),
        ("since:2022-10-27", "until:2022-10-28"),
        ("since:2022-10-28", "until:2022-10-29"),
        ("since:2022-10-29", "until:2022-10-30"),
        ("since:2022-10-30", "until:2022-10-31"),
        ("since:2022-10-31", "until:2022-11-01"),
        ("since:2022-11-01", "until:2022-11-02"),
        ("since:2022-11-02", "until:2022-11-03"),
        ("since:2022-11-03", "until:2022-11-04"),
        ("since:2022-11-04", "until:2022-11-05"),
        ("since:2022-11-05", "until:2022-11-06"),
        ("since:2022-11-06", "until:2022-11-07"),
        ("since:2022-11-07", "until:2022-11-08"),
        ("since:2022-11-08", "until:2022-11-09"),
        ("since:2022-11-09", "until:2022-11-10"),
        ("since:2022-11-10", "until:2022-11-11"),
        ("since:2022-11-11", "until:2022-11-12"),
        ("since:2022-11-12", "until:2022-11-13"),
        ("since:2022-11-13", "until:2022-11-14"),
        ("since:2022-11-14", "until:2022-11-15")
    ]
    QUERY = "airdrop"
    MAX_RESULTS = None # NOTE: Set this to an integer value (i.e., 1000) if you want to limit the amount of tweets scraped per subprocess -- good for testing.
    BASE_OUTFILE_LOCATION = "airdrop_tweets_"
    
    for dayNumber, sinceUntil in enumerate(DAYS_LIST):
        subprocess.Popen(
            Process(
                QUERY,
                sinceUntil[0],
                sinceUntil[1],
                MAX_RESULTS,
                BASE_OUTFILE_LOCATION + f"{dayNumber + 1}.json",
                progress=False
            ).getProcessArgs(),
            shell=True
        )
        time.sleep(1) # NOTE: When in doubt, simply sleep a bit until the computer is happy and ready to do more work :)


if __name__ == "__main__":
    scrape()