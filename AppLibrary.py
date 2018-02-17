import os
import sys
import json
import time
from datetime import datetime, timedelta
import tweepy
import pyspeedtest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import env_variable

cwd = os.getcwd() # cwd = current work directory

def configureApi():
    # Fill in the values noted in previous step here
    cfg = json.load(open(cwd + '/twitter_config.json'))

    auth = tweepy.OAuthHandler(cfg['consumer_key'], cfg['consumer_secret'])
    auth.set_access_token(cfg['access_token'], cfg['access_token_secret'])
    api = tweepy.API(auth)
    return api


def postATweet(downloadSpeed, maxDownloadSpeedLimit):
    api = configureApi()
    maxDownloadSpeedLimit = str(maxDownloadSpeedLimit)
    tweet = "My current download speed: " + downloadSpeed + "MB, but my monthly plan promises: " + maxDownloadSpeedLimit + "MB download speed"
    status = api.update_status(status=tweet)
    json_str = json.dumps(status._json)
    data = json.loads(json_str)
    print 'Successfully tweeted! Tweet Id:', data['id']
    print 'Link:' + env_variable.linkToTwitter + str(data['id'])
    with open(cwd + '\status.json', 'w') as outfile:
        json.dump(data, outfile)
    return str(data['id'])

def deleteStatusInTwitter():
    api = configureApi()

    status_list = api.user_timeline()
    status = status_list[0]
    json_str = json.dumps(status._json)

    data = json.loads(json_str)
    status = api.destroy_status(id=data['id'])
    result = str(data['id']) + ' ' + str(data['text']) + ' is deleted'
    return result

def openLinkInBrowser(tweetId, downloadSpeed):
    driver = webdriver.Chrome()
    driver.get(env_variable.linkToTwitter + tweetId)
    try:
        elem = driver.find_element_by_class_name("TweetTextSize--jumbo")

        time.sleep(3)
        if downloadSpeed in elem.text:
            print "Visual Confirmation: Verified!"
        else:
            print "Visual Confirmation: FAILED"
            print "Actual text in UI:", elem.text[:40], '...'
        driver.quit()
    except:
        print 'openLinkInBrowser function failed. Exception Thrown'
        driver.quit()

def askUserToProvideASL(maxDownloadSpeedLimit):
    maxDownloadSpeedLimit = float(maxDownloadSpeedLimit)
    tryAgain = True
    while tryAgain:
        try:
            userInput = raw_input('Enter the MINIMUM acceptable speed or type "quit" to close the application: ' +'\n')
            if userInput.lower().strip(' ') == 'quit':
                return None
                sys.exit()

            userInput = float(userInput)

            if userInput >= maxDownloadSpeedLimit:
                print 'Maximum expected speed is:', maxDownloadSpeedLimit, 'ASL should be less than', maxDownloadSpeedLimit, '\n'
                tryAgain = True
            elif userInput <= 0.0:
                print 'Minimum acceptable speed can NOT be less than 0 or equal to' + '\n'
                tryAgain = True
            else:
                print '-----------------------------------------------------------------------'
                print userInput, 'is accepted as ASL'
                tryAgain = False
                return userInput
        except:
            if userInput == '':
                print '\n', 'Input value can not be Null/Empty', '\n'
            else:
                # if len(userInput) > 10:
                #     print '"' + userInput[:10] + '..."', 'can not be accepted. You can enter only numbers, please try again'
                # else:
                print '"', userInput, '"', 'can not be accepted. You can enter only numbers, please try again', '\n'
            tryAgain = True

def askUserToProvideTotalNumberOfTestsToRun():
    tryAgain = True
    while tryAgain:
        userInput = raw_input('How many times would you like to run tests: ' + '\n')

        if userInput.lower().strip(' ') == 'quit':
            print '\n' + 'Thank you for using Test And Report Internet Speed app!'
            sys.exit()
        try:
            userInput = int(userInput)

            if len(str(userInput)) > 2:
                print 'Total number of test runs can not be more than 2 digits. Try again.' + '\n'
                tryAgain = True
            elif userInput <= 0:
                print 'Total number of test runs can NOT be equal to 0 or less' + '\n'
                tryAgain = True
            else:
                print '-----------------------------------------------------------------------'
                print userInput, 'is accepted'
                tryAgain = False

                totalNumberOfTestsToRun = userInput
                return totalNumberOfTestsToRun
        except:
            if userInput == '':
                print '\n', 'Input value can not be Null/Empty', '\n'
            else:
                print '"', userInput, '"', 'can not be accepted. You can enter only full numbers, please try again', '\n'
            tryAgain = True
      
def askUserToProvideMaxDownloadSpeedLimit():
    tryAgain = True
    while tryAgain:
        try:
            userInput = raw_input('Enter the MAXIMUM internet download speed: ' + '\n')

            userInput = int(userInput)

            if len(str(userInput)) > 3:
                print 'Maximum download speed should not be more than 3 digits. Try again.' + '\n'
                tryAgain = True
            elif userInput <= 0:
                print 'Maximum download speed can NOT be less than 0 or equal to' + '\n'
                tryAgain = True
            else:
                print '-----------------------------------------------------------------------'
                print userInput, 'is accepted as maximum download speed limit'
                tryAgain = False

                maxDownloadSpeedLimit = userInput
                return maxDownloadSpeedLimit
        except:
            if userInput == '':
                print '\n', 'Input value can not be Null/Empty', '\n'
            else:
                print '"', userInput, '"', 'can not be accepted. You can enter only full numbers, please try again', '\n'
            tryAgain = True

def runSpeedTest():
    speedTest = pyspeedtest.SpeedTest()
    try:
        downloadSpeed = float(round(speedTest.download()/1048576, 2))
        return downloadSpeed
    except:
        print 'Speed Test failed. Please check your internet connection'
        return None

def testAndDisplayTestResults(maxDownloadSpeedLimit):
    acceptableSpeedLimit = askUserToProvideASL(maxDownloadSpeedLimit)

    if acceptableSpeedLimit is None:
        print '\n' + 'Thank you for using Test And Report Internet Speed app!'
        sys.exit()
    print 'speedtest.net in progress..'
    try:
        speedTestResult = runSpeedTest()
        if speedTestResult is not None:
            print str(datetime.now())
            print '\n', 'Current download speed:', speedTestResult
            if speedTestResult <= acceptableSpeedLimit:
                print '#########################################'
                print "DOWNLOAD SPEED:", speedTestResult, ". This data is being posted to Twitter."
                downloadSpeed = str(speedTestResult)
                tweetId = postATweet(downloadSpeed, maxDownloadSpeedLimit)
                print '#########################################'
                openLinkInBrowser(tweetId, downloadSpeed)
            return True
    except:
        print 'testAndDisplayTestResults function failed. Exception Thrown'
        return False

def speedTestOrganizer(maxNumberOfTests):
    maxDownloadSpeedLimit = askUserToProvideMaxDownloadSpeedLimit()

    counter = 0
    while counter < maxNumberOfTests:
        print '\n', 'TEST #', counter + 1, 'STARTED'
        result = testAndDisplayTestResults(maxDownloadSpeedLimit)
        if result:
            print 'END OF TEST'
            if maxNumberOfTests != counter:
                print 'Next test will be performed in 5 second'
                print '-----------------------------------------------------------------------'
                time.sleep(5)
            counter += 1
        else:
            print 'Test #', counter + 1, 'Failed, test will start again in 2 seconds'
            time.sleep(2)
            print '\n', 'TEST FAILED'
            print '-----------------------------------------------------------------------'
    if counter == maxNumberOfTests:
            print 'Default maxNumberOfTests set to:', maxNumberOfTests, ', and you reached the max run limit'
            print 'Run app again if you would to test internet speed more'
            sys.exit()

def testSpeedAndReport():
    print 'This app tests internet speed. Internet provider should provide 70MB download speed maximum.'
    print 'Maximum download speed varies on every user based on purchased plan.'
    print 'Check your internet service contract details to find out your maximum download speed.'
    print 'When you run this app, app asks you to provide acceptable speed limit(ASL) and '
    print 'it tests whether current speed is equal to or more from provided ASL.'
    print 'if test result is less than ASL then this app generates twitter post with test result.'
    print 'Otherwise, it simply displays test results without posting it in twitter.' + '\n'

    maxNumberOfTests = 10
    start = True
    while start:
        userInput = raw_input('Enter number 1 to start the app: ')
        if userInput.lower().strip(' ') == 'quit':
            print '\n' + 'Thank you for using Test And Report Internet Speed app!'
            exit()
        try:
            userInput = int(userInput)
            if userInput == 1:
                print '-----------------------------------------------------------------------'
                speedTestOrganizer(maxNumberOfTests)
                start = False
        except ValueError:
            if userInput == '':
                print '\n','Input value can not be Null/Empty', '\n'

        print '"', userInput, '"', 'can not be accepted. You can enter only number 1 to start the app, please try again'
        print '-----------------------------------------------------------------------'
        start = True

def deleteLastFiveTweets():
    counter = 5
    i = 1
    try:
        while i <= counter:
            result = deleteStatusInTwitter()
            print i, result
            i += 1
    except:
        print 'No More Tweet To Delete'


def askUserToProvideLengthOfInterval():
    tryAgain = True
    while tryAgain:
        userInput = raw_input('How often would you like to run speed test? (In minutes)' '\n')
        if userInput.isdigit():
            if int(userInput) <= 0:
                print 'It should be more than 0'
            elif len(userInput) < 3:
                print userInput, 'is accepted. Test will run every', userInput, 'minutes'
                tryAgain = False
                return userInput
            else:
                print 'You can not enter more than 2 digits. 99 is the highest number to enter'
                tryAgain = True
        else:
            print '"', userInput, '"', 'can not be accepted. You can enter only full numbers, please try again', '\n'
            tryAgain = True


def runSpeedTestWithIntervals_old():
    numberOfTests = askUserToProvideTotalNumberOfTestsToRun()
    interval = int(askUserToProvideLengthOfInterval())
    maxDownloadSpeed = askUserToProvideMaxDownloadSpeedLimit()
    asl = askUserToProvideASL(maxDownloadSpeed)
    if asl is None:
        print 'Thank you for using Test And Report Internet Speed app!'
        sys.exit()
    i = 0
    while i < numberOfTests:
        print 'TEST #', i+1, 'STARTED.', 'TOTAL NUMBER OF TESTS TO RUN:', numberOfTests
        downloadSpeed = runSpeedTest()
        if downloadSpeed is not None:
            downloadSpeed = str(downloadSpeed)
            print 'Current download speed:', downloadSpeed
            if float(downloadSpeed) <= asl:
                tweetId = postATweet(downloadSpeed, maxDownloadSpeed)
                openLinkInBrowser(tweetId, downloadSpeed)
            print 'TEST #', i + 1, 'ENDED'
            i += 1

            if numberOfTests != i:
                nextTestTime = datetime.now() + timedelta(minutes=interval)
                print '\n' 'next test will run in', interval, 'mins, at:', '{:%H:%M:%S}'.format(nextTestTime)
                print '-----------------------------------------------------------------------'
                time.sleep(interval * 60)
        else:
            print 'Test #', i+1, 'Failed. App will re-try to test again in 5 seconds'
            time.sleep(5)
            print '\n', 'TEST FAILED'
            print '-----------------------------------------------------------------------'

    print 'Thank you for using Test And Report Internet Speed app!'

def runSpeedTestWithIntervals():
    numberOfTests = askUserToProvideTotalNumberOfTestsToRun()
    interval = int(askUserToProvideLengthOfInterval())
    maxDownloadSpeed = askUserToProvideMaxDownloadSpeedLimit()
    asl = askUserToProvideASL(maxDownloadSpeed)
    if asl is None:
        print 'Thank you for using Test And Report Internet Speed app!'
        sys.exit()
    i = 0
    testRunTimeWithTestResultDictionary = {}
    while i < numberOfTests:
        print 'TEST #', i+1, 'STARTED.', 'TOTAL NUMBER OF TESTS TO RUN:', numberOfTests
        # downloadSpeed = runSpeedTest()
        downloadSpeed = 14.14
        if downloadSpeed is not None:
            downloadSpeed = str(downloadSpeed)
            print 'Current download speed:', downloadSpeed
            if float(downloadSpeed) <= asl:
                # tweetId = postATweet(downloadSpeed, maxDownloadSpeed)
                # openLinkInBrowser(tweetId, downloadSpeed)
                pass
            print 'TEST #', i + 1, 'ENDED'
            i += 1

            nextTestTime = datetime.now() + timedelta(seconds=interval)
            testCompleteTime = '{:%H:%M:%S}'.format(nextTestTime)

            if numberOfTests != i:
                print '\n' 'next test will run in', interval, 'mins, at:', testCompleteTime
                print '-----------------------------------------------------------------------'
                # time.sleep(interval * 60)
                time.sleep(interval)

            testRunTimeWithTestResultDictionary[i] = {'Test': i, 'downloadSpeed': downloadSpeed, 'time': testCompleteTime}

        else:
            print 'Test #', i+1, 'Failed. App will re-try to test again in 5 seconds'
            time.sleep(5)
            print '\n', 'TEST FAILED'
            print '-----------------------------------------------------------------------'

    print '\nSUMMARY:'
    print 'Max Download Speed:', str(maxDownloadSpeed) + 'MB | Acceptable Speed Limit:', str(asl) + 'MB'
    print numberOfTests, 'tests are executed with', interval, '- minute interval.'
    for keys in testRunTimeWithTestResultDictionary:
        print testRunTimeWithTestResultDictionary[keys]

    print '\nThank you for using "The Test And Report Internet Speed" app!'