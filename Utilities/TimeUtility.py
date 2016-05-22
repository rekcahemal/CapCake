#####################################################################################################
#####################################################################################################
## Created on Aug 29, 2013
## @author: Gerasimos Kassaras
## E-mail: g.kassaras@gmail.com
## Nickname: Lamehacker Free Industries
## 
## Comment: This class is used to do time related jobs. 
#######################################################################################################
#######################################################################################################

from time import gmtime, strftime
import time

class timeUtility(object):

    def __init__(self):
        self.time = strftime("%Y-%m-%d %H:%M:%S", gmtime())# Get current time.
        self.delay = 10 # Default 10 seconds of delay.
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------
    '''
    Description: This function simply returns nothing and adds a delay.
    Status: Finished.
    Usage: This is going to be used by many other modules.
    '''
    def getDelay(self): # Gets as an input nothing and generates a delay.
        time.sleep(self.delay)
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------
    def getTimeForLogging(self): # Gets as an input nothing and returns the time in string.
        '''
        Description: This function simply returns the time in the format of [hour:minutes:seconds:day:month:year] for logging reasons.
        Status: Finished.
        Usage: This is going to initialize the time class.
        '''
        return '['+self.time+'] '
