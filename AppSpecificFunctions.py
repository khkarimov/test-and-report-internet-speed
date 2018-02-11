import os
import sys
import json
import time
from datetime import datetime
import tweepy
import pyspeedtest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

cwd = os.getcwd() # cwd = current work directory

def configureApi():
    # Fill in the values noted in previous step here
    cfg = json.load(open(cwd + '/tweeter_config.json'))

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
    with open(cwd + '\status.json', 'w') as outfile:
        json.dump(data, outfile)
    return str(data['id'])

def deleteStatusInTweeter():
    api = configureApi()

    status_list = api.user_timeline()
    status = status_list[0]
    json_str = json.dumps(status._json)

    data = json.loads(json_str)
    print data['id'], data['text'], 'is deleted'
    status = api.destroy_status(id=data['id'])

def openLinkInBrowser(tweetId, downloadSpeed):
    driver = webdriver.Chrome()
    driver.get("https://twitter.com/ComcastUser3301/status/" + tweetId)
    elem = driver.find_element_by_class_name("TweetTextSize--jumbo")

    time.sleep(3)
    if downloadSpeed in elem.text:
        print "UI test: PASSED"
    else:
        print "UI test: FAILED"
        print "Actual text in UI:", elem.text[:40], '...'
    driver.quit()

def askUserToProvideASTL(maxDownloadSpeedLimit):
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



def test_and_write_speed(maxDownloadSpeedLimit):
    acceptableSpeedLimit = askUserToProvideASTL(maxDownloadSpeedLimit)

    if acceptableSpeedLimit is None:
        print '\n' + 'Thank you for using "Report Your Low Speed To Comcast" app!'
        sys.exit()
    print 'speedtest.net in progress..'
    try:
        speedTestResult = runSpeedTest()
        if speedTestResult is not None:
            print str(datetime.now())
            print '\n', 'Current download speed:', speedTestResult
            if speedTestResult <= acceptableSpeedLimit:
                print '#########################################'
                print "DOWNLOAD SPEED:", speedTestResult, ". This data is being posted to Tweeter."
                downloadSpeed = str(speedTestResult)
                tweetId = postATweet(downloadSpeed, maxDownloadSpeedLimit)
                print "Link: https://twitter.com/ComcastUser3301/status/" + tweetId
                print '#########################################'
                openLinkInBrowser(tweetId, downloadSpeed)
            return True
    except:
        print 'EXCEPTION THROWN IN test_and_write_speed function'
        return False

def scheduled_speed_test(maxNumberOfTests):
    maxDownloadSpeedLimit = askUserToProvideMaxDownloadSpeedLimit()

    counter = 1
    while counter < maxNumberOfTests:
        print '\n', 'TEST #', counter, 'STARTED'
        result = test_and_write_speed(maxDownloadSpeedLimit)
        if result:
            print 'END OF TEST'
            if maxNumberOfTests != counter:
                print 'Next test will be performed in 5 second'
                print '-----------------------------------------------------------------------'
                time.sleep(5)
            counter += 1
        else:
            print 'Test #', counter, 'Failed, will try again in 2 seconds'
            time.sleep(2)
            print '\n', 'TEST FAILED'
            print '-----------------------------------------------------------------------'
    if counter == maxNumberOfTests:
            print 'Default maxNumberOfTests set to:', maxNumberOfTests - 1, ', and you reached the max run limit'
            print 'Run app again if you would to test internet speed more'
            sys.exit()

def testSpeedAndReport():
    print 'This app tests internet speed. Internet provider should provide 70MB download speed maximum.'
    print 'Maximum download speed varies on every user based on purchased plan.'
    print 'Check your internet service contract details to find out your maximum download speed.'
    print 'When you run this app, app asks you to provide acceptable speed limit(ASL) and '
    print 'it tests whether current speed is equal to or more from provided ASL.'
    print 'if test result is less than ASL then this app generates tweeter post with test result.'
    print 'Otherwise, it simply displays test results without posting it in tweeter.' + '\n'

    maxNumberOfTests = 10
    start = True
    while start:
        userInput = raw_input('Enter number 1 to start the app: ')
        if userInput.lower().strip(' ') == 'quit':
            print '\n' + 'Thank you for using "Report Your Low Speed To Comcast" app!'
            exit()
        try:
            userInput = int(userInput)
            if userInput == 1:
                print '-----------------------------------------------------------------------'
                scheduled_speed_test(maxNumberOfTests)
                start = False
        except ValueError:
            if userInput == '':
                print '\n','Input value can not be Null/Empty', '\n'

        print '"', userInput, '"', 'can not be accepted. You can enter only number 1 to start the app, please try again'
        print '-----------------------------------------------------------------------'
        start = True
