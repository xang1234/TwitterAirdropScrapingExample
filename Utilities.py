def aggregateFiles():
    import json
    FILE_PATTERN: str = "tweets/airdrop_tweets_"
    FILE_EXTENSION: str = ".json"
    FILE_COUNT: int = 75
    OUTFILE_LOCATION: str = "tweets/aggregated_tweets.json"

    allTweetsJson: list[dict] = []

    for dayNumber in range(1, FILE_COUNT + 1):
        currentFile: str = f"{FILE_PATTERN}{dayNumber}{FILE_EXTENSION}"
        with open(currentFile, 'r') as infile:
            for line in infile.readlines():
                allTweetsJson.append(json.loads(line))
    
    with open(OUTFILE_LOCATION, 'w') as outfile:
        for tweetJson in allTweetsJson:
            json.dump(tweetJson, outfile)
            outfile.write('\n')
    
    print(len(allTweetsJson))

def loadDataFromFile(filepath: str, dataLimit: int = None) -> dict:
    dataDict: dict = {}
    with open(filepath, 'r', encoding='utf-8') as dataFile:
        for line in dataFile.readlines()[:dataLimit]:
            count, content = line.strip().split(' | ')
            dataDict[content.strip()] = int(count.strip())

    return dataDict

def plotFileData(data: dict, plotTitle: str = None, xLabel: str = None, yLabel: str = None, maxPlotXSize: int = None) -> None:
    """
    Plots a matplotlib.pyplot bar chart with the provided data.

    Arguments
        [Required] data: dict
            The data that will be plotted
        [Optional] plotTitle: str
            The title for the plot
        [Optional] xTitle: str
            The plot label for the x-axis
        [Optional] yTitle: str
            The plot label for the y-axis
        [Optional] maxPlotSize: int
            Determines the max x-range of data that will be plotted.
    """
    import matplotlib.pyplot as plt
    xContent, yCounts = zip(*sorted(data.items(), key = lambda kv: kv[1], reverse=True)[:maxPlotXSize])
    plt.rc('font', size=8)
    plt.rc('axes', titlesize=12)
    plt.rc('axes', labelsize=10)
    plt.subplots(figsize=(16, 8))
    plt.tight_layout(rect=[0.1,0.1,0.9, 0.95])
    plt.xticks(range(len(xContent)), xContent, rotation=45, ha="right")
    if plotTitle:
        plt.title(plotTitle)
    if xLabel:
        plt.xlabel(xLabel)
    if yLabel:
        plt.ylabel(yLabel)
    plt.bar(range(len(xContent)), yCounts)
    plt.show()
    
def plotFourFileData(
    dataTopLeft:                dict,
    dataTopRight:               dict,
    dataBottomLeft:             dict,
    dataBottomRight:            dict,
    plotTitleTopLeft:           str = None,
    plotTitleTopRight:          str = None,
    plotTitleBottomLeft:        str = None,
    plotTitleBottomRight:       str = None,
    xLabelTopLeft:              str = None,
    xLabelTopRight:             str = None,
    xLabelBottomLeft:           str = None,
    xLabelBottomRight:          str = None,
    yLabelTopLeft:              str = None,
    yLabelTopRight:             str = None,
    yLabelBottomLeft:           str = None,
    yLabelBottomRight:          str = None,
    maxPlotXSizeTopLeft:        int = None,
    maxPlotXSizeTopRight:       int = None,
    maxPlotXSizeBottomLeft:     int = None,
    maxPlotXSizeBottomRight:    int = None,
    titleFontSize:              int = 12,
    axesLabelFontSize:          int = 10,
    tickLabelFontSize:          int = 7
):
    import matplotlib.pyplot as plt    
    fig, ((axesTopLeft, axesTopRight), (axesBottomLeft, axesBottomRight)) = plt.subplots(2, 2, figsize=(24, 10))
    fig.canvas.manager.set_window_title('Twitter Airdrop Data')

    dataList =          [dataTopLeft,           dataTopRight,           dataBottomLeft,         dataBottomRight]
    titleList =         [plotTitleTopLeft,      plotTitleTopRight,      plotTitleBottomLeft,    plotTitleBottomRight]
    xLabelList =        [xLabelTopLeft,         xLabelTopRight,         xLabelBottomLeft,       xLabelBottomRight]
    yLabelList =        [yLabelTopLeft,         yLabelTopRight,         yLabelBottomLeft,       yLabelBottomRight]
    maxPlotXSizeList =  [maxPlotXSizeTopLeft,   maxPlotXSizeTopRight,   maxPlotXSizeBottomLeft, maxPlotXSizeBottomRight]

    for i, ax in enumerate([axesTopLeft, axesTopRight, axesBottomLeft, axesBottomRight]):
        data, plotTitle, xLabel, yLabel, maxPlotXSize = dataList[i], titleList[i], xLabelList[i], yLabelList[i], maxPlotXSizeList[i]
        xContent, yCounts = zip(*sorted(data.items(), key = lambda kv: kv[1], reverse=True)[:maxPlotXSize])
        ax.bar(xContent, yCounts)
        ax.set_xticks(range(len(xContent)), xContent, rotation=45, ha="right")
        if plotTitle:
            ax.set_title(plotTitle)
        if xLabel:
            ax.set_xlabel(xLabel)
        if yLabel:
            ax.set_ylabel(yLabel)
        ax.title.set_fontsize(titleFontSize)
        ax.xaxis.label.set_fontsize(axesLabelFontSize)
        ax.yaxis.label.set_fontsize(axesLabelFontSize)
        for label in ax.get_xticklabels() + ax.get_yticklabels():
            label.set_fontsize(tickLabelFontSize)

    plt.subplots_adjust(left=0.05, bottom=0.1, right=0.975, top=0.975, wspace=0.1, hspace=0.3)
    plt.show()

if __name__ == "__main__":
    FILES = {
        "W": "data/word_frequencies.txt",
        "TA": "data/tweet_author_frequencies.txt",
        "H": "data/hashtag_frequencies.txt",
        "UM": "data/username_mention_frequencies.txt"
    }

    # NOTE: File aggregation
    # aggregateFiles()

    # NOTE: File Loading
    WORD_DATA_MAX_SIZE: int = 30
    TWEET_AUTHOR_DATA_MAX_SIZE: int = 30
    HASHTAG_DATA_MAX_SIZE: int = 30
    USERNAME_MENTION_DATA_MAX_SIZE: int = 30
    wordFileData = loadDataFromFile(FILES['W'], dataLimit=WORD_DATA_MAX_SIZE)
    tweetAuthorFileData = loadDataFromFile(FILES['TA'], dataLimit=TWEET_AUTHOR_DATA_MAX_SIZE)
    hashtagFileData = loadDataFromFile(FILES['H'], dataLimit=HASHTAG_DATA_MAX_SIZE)
    usernameMentionFileData = loadDataFromFile(FILES['UM'], dataLimit=USERNAME_MENTION_DATA_MAX_SIZE)

    # Removing the ids from tweetAuthorFrequencies
    tweetAuthorFileData = {k.split()[0]: v for k, v in tweetAuthorFileData.items()}
  
    # NOTE: Plotting four chart file data
    plotFourFileData(
        # Data [Top-Left, Top-Right, Bottom-Left, Bottom-Right]
        dataTopLeft=wordFileData,
        dataTopRight=tweetAuthorFileData,
        dataBottomLeft=hashtagFileData,
        dataBottomRight=usernameMentionFileData,

        # Titles [Top-Left, Top-Right, Bottom-Left, Bottom-Right]
        plotTitleTopLeft="Word Frequencies",
        plotTitleTopRight="Tweet Author Frequencies",
        plotTitleBottomLeft="Hashtag Frequencies",
        plotTitleBottomRight="Username Mention Frequencies",

        # X-Axis Labels [Top-Left, Top-Right, Bottom-Left, Bottom-Right]
        xLabelTopLeft=None,
        xLabelTopRight=None,
        xLabelBottomLeft=None,
        xLabelBottomRight=None,

        # Y-Axis Labels [Top-Left, Top-Right, Bottom-Left, Bottom-Right]
        yLabelTopLeft=None,
        yLabelTopRight=None,
        yLabelBottomLeft=None,
        yLabelBottomRight=None,

        # Max Plot X Sizes [Top-Left, Top-Right, Bottom-Left, Bottom-Right]
        maxPlotXSizeTopLeft=None,
        maxPlotXSizeTopRight=None,
        maxPlotXSizeBottomLeft=None,
        maxPlotXSizeBottomRight=None
    )   

    # NOTE: Plotting single chart file data
    # plotFileData(hashtagFileData, "Hashtag Data", "Hashtags", "Frequencies", WORD_DATA_MAX_SIZE)
