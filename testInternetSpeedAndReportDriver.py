import os
import sys
from AppSpecificFunctions import *

# Un-comment deleteStatusInTweeter() function if you would like to delete last 10 tweets from you accounts
i = 1
while i < 10:
    deleteStatusInTweeter()
    i += 1

# This functions tests internet speed and reports the results in tweet if internet speed is lower than expected.
# testSpeedAndReport()
