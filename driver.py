import os
import sys
import datetime
import time
from AppLibrary import *

# This functions tests internet speed and reports the results in tweet if internet speed is lower than expected.
# testSpeedAndReport()

numberOfTests = askUserToProvideTotalNumberOfTestsToRun()
maxDownloadSpeed = askUserToProvideMaxDownloadSpeedLimit()
asl = askUserToProvideASL(maxDownloadSpeed)
i = 0
while i < numberOfTests:
    print 'TEST #', i+1, 'STARTED'
    downloadSpeed = runSpeedTest()
    if downloadSpeed is not None:
        downloadSpeed = str(downloadSpeed)

        print 'Current download speed:', downloadSpeed
        tweetId = postATweet(downloadSpeed, maxDownloadSpeed)
        openLinkInBrowser(tweetId, downloadSpeed)
        print 'TEST #', i + 1, 'ENDED'
        i += 1

        if numberOfTests != i:
            print '\n' 'next test will run in 5 mins'
            print str(datetime.now())
            print '-----------------------------------------------------------------------'
            # time.sleep((5*60))
            time.sleep(10)
    else:
        print 'Test #', i+1, 'Failed. App will re-try to test again in 2 seconds'
        time.sleep(2)
        print '\n', 'TEST FAILED'
        print '-----------------------------------------------------------------------'



