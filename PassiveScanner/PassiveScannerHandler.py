#####################################################################################################
#####################################################################################################
## Created on Sep 14, 2013
## @author: Gerasimos Kassaras
## E-mail: g.kassaras@gmail.com
## Nickname: Lamehacker Free Industries
## 
## Comment: This class is used to handle all connections and should accept feed from the command line. 
#######################################################################################################
#######################################################################################################

import LogManager.LogHandler

passiveScannerLogger = LogManager.LogHandler.loggingHandler()# logs info,warning,error,critical,debug events.

class passiveScannerHandler:
        '''
        Description: This class is going to be used to identify vulnerabilities by passively testing the site.
        Status: In progress.
        Usage: This class is used to implement all standard methods to describe vulnerabilities.
        '''
        
        def __init__(self):
            '''
            Description: This initializes the Scanner.
            Status: In progress.
            Usage: This is used to initialize the all needed information to connect to the http/https server.
            '''
            
            passiveScannerLogger.logInfo("--------------------------------------------------------------------------------------------------------")            
            passiveScannerLogger.logInfo("---< Package: PassiveScanner - Module: PassiveScannerHandler Class: passiveScannerHandler Initiated >---")
            passiveScannerLogger.logInfo("--------------------------------------------------------------------------------------------------------")