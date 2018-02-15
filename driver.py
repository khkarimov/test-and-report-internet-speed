import os
import sys
import datetime
import time
from AppLibrary import *

# This functions tests internet speed and reports the results in tweet if internet speed is lower than expected.
# testSpeedAndReport()

def askUserToProvideLengthOfInterval():
    tryAgain = True
    while tryAgain:
        userInput = raw_input('How often would you like to run speed test? (In minutes)' '\n')
        if userInput.isdigit():
            if int(userInput) <= 0:
                print 'It should be more than 0'
            elif len(userInput) < 3:
                print userInput, 'is accepted. Test will be run every', userInput, 'minutes'
                tryAgain = False
                return userInput
            else:
                print 'You can not enter more than 2 digits. 99 is the highest number to enter'
                tryAgain = True
        else:
            print '"', userInput, '"', 'can not be accepted. You can enter only full numbers, please try again', '\n'
            tryAgain = True

# askUserToProvideLengthOfInterval()

def runSpeedTestWithInterval():
    numberOfTests = askUserToProvideTotalNumberOfTestsToRun()
    interval = int(askUserToProvideLengthOfInterval())
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
                print '\n' 'next test will run in', interval, 'mins'
                print str(datetime.now())
                print '-----------------------------------------------------------------------'
                time.sleep(interval * 60)
        else:
            print 'Test #', i+1, 'Failed. App will re-try to test again in 5 seconds'
            time.sleep(5)
            print '\n', 'TEST FAILED'
            print '-----------------------------------------------------------------------'

    print 'Thank you for using Test And Report Internet Speed app!'


runSpeedTestWithInterval()