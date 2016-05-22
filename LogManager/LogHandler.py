#####################################################################################################
#####################################################################################################
## Created on Sep 01, 2013
## @author: Gerasimos Kassaras
## E-mail: g.kassaras@gmail.com
## Nickname: Lamehacker Free Industries
## 
## Comment: This class is used as a centralized logger for the scanner
#######################################################################################################
#######################################################################################################

import logging
from bs4 import UnicodeDammit

genericLoggerName = 'CapCake_logger'
genericLogger = logging.getLogger(genericLoggerName)
genericLoggerHandler = logging.FileHandler('CapCake_logger.log')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
genericLoggerHandler.setFormatter(formatter)
genericLogger.addHandler(genericLoggerHandler)
genericLogger.setLevel(logging.DEBUG)

class loggingHandler: # logs info,warning,error,critical,debug events.

    def __init__(self):
        '''
        Description: This class is used to manage the logging information from the scanner.
        Status: Finished.
        Usage: This is used to initialize with the proper logging level.
        '''
        self.logInfo("--- Package: LoggingManager - Module: LoggingHandler Class: loggingHandler Initiated ---")
    
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------
    def logInfo(self,msg):
        genericLogger.info(msg)
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------
    def logWarning(self,msg):
        genericLogger.warn(msg,exc_info=True)
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------
    def logError(self,msg):
        genericLogger.error(msg,exc_info=True)
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------
    def logCritical(self,msg):
        genericLogger.critical(msg,exc_info=True)
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------
    def logDebug(self,msg):
        genericLogger.debug(msg)