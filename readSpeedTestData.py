import os
import sys
import json
from Naked.toolshed.shell import execute_js, muterun_js
import time
from datetime import datetime
import tweepy
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

cwd = os.getcwd() # cwd = current work directory
print cwd

def configureApi():
    # Fill in the values noted in previous step here
    cfg = json.load(open(cwd + '/tweeter_config.json'))

    auth = tweepy.OAuthHandler(cfg['consumer_key'], cfg['consumer_secret'])
    auth.set_access_token(cfg['access_token'], cfg['access_token_secret'])
    api = tweepy.API(auth)
    return api


def postATweet(downloadSpeed):
    api = configureApi()
    tweet = "My current download speed: " + downloadSpeed + "MB, but my monthly plan promises 70MB download speed"
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

def askUserToProvideASTL():
    tryAgain = True
    while tryAgain:
        try:
            userInput = raw_input('Enter the minimum acceptable speed: ' +'\n')
            if userInput == 'seventy':
                print 'You typed 70 and i take it BUT never test like that! i make an exception this time just to confuse as fuck'
                tryAgain = False
                userInput = 70
            elif userInput == 'quit':
                return None
                sys.exit()
            # elif len(userInput) > 6:
            #     tryAgain = False
            #     print 'The length of your input can not be more than 6 digits'
            #     sys.exit(1)
            userInput = float(userInput)

            if userInput >= 70.00:
                print 'Maximum expected speed is 70Mb. ASL should be less than 70Mb.' + '\n'
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
                print '\n', '\n', '\n', 'I KNEW YOU WOULD TRY TO PASS NULL, YOU SNEAKY FUCK! I GOT YOU, YOU POOR BUSTARD! :)', '\n', '\n', '\n'
            else:
                # if len(userInput) > 10:
                #     print '"' + userInput[:10] + '..."', 'can not be accepted. You can enter only numbers, please try again'
                # else:
                print '"' + userInput + '"', 'can not be accepted. You can enter only numbers, please try again', '\n'
            tryAgain = True


def test_and_write_speed():
    acceptableSpeedLimit = askUserToProvideASTL()

    if acceptableSpeedLimit is None:
        print '\n' + 'Thank you for using "Report Your Low Speed To Comcast" app!'
        sys.exit()
    print 'speedtest.net in progress..'
    response = execute_js(cwd + '\dev\speedtest.js')
    data = json.load(open(cwd + '\speedTestResult.json'))
    try:
        if 'ENOTFOUND' not in data:
            print str(datetime.now())
            data = json.load(open(cwd + '\speedTestResult.json'))
            print 'download speed:', data['speeds']['download']
            print 'upload speed:', data['speeds']['upload']

            if float(data['speeds']['download']) <= acceptableSpeedLimit:
                print '#########################################'
                print "DOWNLOAD SPEED:", data['speeds']['download'], ". This data is being posted to Tweeter."
                downloadSpeed = str(data['speeds']['download'])
                tweetId = postATweet(downloadSpeed)
                print "Link: https://twitter.com/ComcastUser3301/status/" + tweetId
                print '#########################################'
                openLinkInBrowser(tweetId, downloadSpeed)
            return True
    except:
        print 'EXCEPTION THROWN IN test_and_write_speed function'
        return False

def scheduled_speed_test(maxNumberOfTests):
    counter = 1
    while counter <= maxNumberOfTests:
        print '\n', 'TEST #', counter, 'STARTED'
        result = test_and_write_speed()
        if result:
            print 'END OF TEST'
            if maxNumberOfTests != counter:
                print 'Next test will be performed in 10 second'
                print '-----------------------------------------------------------------------'
                time.sleep(2)
            counter += 1
        else:
            print 'Test #', counter, 'Failed, will try again in 5 seconds'
            time.sleep(1)
            print '\n', 'TEST FAILED'
            print '-----------------------------------------------------------------------'


def intro():
    print 'This app tests internet speed. Comcast should provide 70MB maximum speed. '
    print 'When you run this app, app asks you to provide acceptable speed limit(ASL) and '
    print 'it tests whether current speed is equal to or more from provided ASL.'
    print 'if test result is less than ASL then this app should generate a twitter with test result.'
    print 'Otherwise, it simply displays test results' + '\n'

    maxNumberOfTests = 100
    start = True
    while start:
        userInput1 = raw_input('Enter number 1 to start the app: ')
        if userInput1 == 'quit':
            print '\n' + 'Thank you for using "Report Your Low Speed To Comcast" app!'
            exit()
        try:
            userInput1 = int(userInput1)
            if userInput1 == 1:
                print '-----------------------------------------------------------------------'
                scheduled_speed_test(maxNumberOfTests)
                start = False
        except ValueError:
            if userInput1 == '':
                print '\n', '\n', '\n', 'I KNEW YOU WOULD TRY TO PASS NULL, YOU SNEAKY FUCK! I GOT YOU, YOU POOR BUSTARD! :)', '\n', '\n', '\n'

        print '"', userInput1, '"', 'can not be accepted. You can enter only number 1 to start the app, please try again'
        print '-----------------------------------------------------------------------'
        start = True

intro()

def deleteLastFiveTweets():
    counter = 13
    i = 1
    try:
        while i < counter:
            i, deleteStatusInTweeter()
            i += 1
    except:
        print 'No More Tweet To Delete'

# deleteLastFiveTweets()