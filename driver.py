import os
import sys
from AppLibrary import *

# This functions tests internet speed and reports the results in tweet if internet speed is lower than expected.
# testSpeedAndReport()

maxDownloadSpeed = askUserToProvideMaxDownloadSpeedLimit()
asl = askUserToProvideASL(maxDownloadSpeed)
downloadSpeed = runSpeedTest()
postATweet(downloadSpeed, maxDownloadSpeed)