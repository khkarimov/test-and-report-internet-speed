import os
import sys
from AppSpecificFunctions import *

# Un-comment deleteStatusInTweeter() function if you would like to delete last 10 tweets from you accounts
def deleteLastFiveTweets():
    counter = 5
    i = 1
    try:
        while i < counter:
            i, deleteStatusInTweeter()
            i += 1
    except:
        print 'No More Tweet To Delete'

deleteLastFiveTweets()

# This functions tests internet speed and reports the results in tweet if internet speed is lower than expected.
# testSpeedAndReport()
