import os
import sys
from AppLibrary import *

# This functions tests internet speed and reports the results in tweet if internet speed is lower than expected.
# testSpeedAndReport()

numberOfTests = askUserToProvideTotalNumberOfTestsToRun()
maxDownloadSpeed = askUserToProvideMaxDownloadSpeedLimit()
asl = askUserToProvideASL(maxDownloadSpeed)
i = 0
while i < numberOfTests:
    print 'TEST #', i+1, 'STARTED'
    downloadSpeed = str(runSpeedTest())
    print 'Current download speed:', downloadSpeed
    tweetId = postATweet(downloadSpeed, maxDownloadSpeed)
    openLinkInBrowser(tweetId, downloadSpeed)
    print 'TEST #', i+1, 'ENDED'
    i += 1
