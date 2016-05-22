#####################################################################################################
#####################################################################################################
## Created on Aug 29, 2013
## @author: Gerasimos Kassaras
## E-mail: g.kassaras@gmail.com
## Nickname: Lamehacker Free Industries
## 
## Comment: This class is used to handle all connections and should accept feed from the command line. 
#######################################################################################################
#######################################################################################################

import socket
import LogManager.LogHandler

connectionLogger = LogManager.LogHandler.loggingHandler()# logs info,warning,error,critical,debug events.

class connnectionHandler:
    '''
    Description: This class manages all scanner connections.
    Status: In progress.
    Usage: This is used to manage all interactions with the web server.
    '''
        
    def __init__(self,domainName,port):
        '''
        Description: This initializes the connection handler class.
        Status: In progress.
        Usage: This is used to test all needed to connect to the server, also change connection attributes.
        '''
        
        self.domainName = domainName # This value is populated from the each inserted url.
        self.port = port # This value is populated from the each inserted url.
        '''
        These variable are going to be used for analyzing the http/https response and identify vulnerabilities.
        '''
        
        connectionLogger.logInfo("--- Package: ConnectionManager - Module: ConnectionHandler Class: connectionHandler Initiated ---")

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------
    def isServerLive(self):# Get as input nothing and returns boolean value is server is live.
        '''
        Description: This function is used to check if the server accessible through the given port.
        Status: Finished.
        Usage: This is used is used as a condition to initiate the scan.
        '''
        
        remoteServerIP = self.domainName
        port = self.port
        
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            result = sock.connect_ex((remoteServerIP, port))

            if result == 0:
                connectionLogger.logInfo('Port in '+remoteServerIP+': is Open :'.format(port))
                sock.close()

                return True

        except socket.timeout:
            connectionLogger.logError('Calling isServerLive() - Server timeout.')

        except socket.gaierror:
            connectionLogger.logError('Calling isServerLive() - Server could not resolve ')

            return False
        
        except socket.error:
            connectionLogger.logError('Calling isServerLive() - Server could not connect.')

            return False
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------
    def getServerIP(self):# Get as input nothing and returns server ip.
        '''
        Description: This function converts the domain name to an IP.
        Status: Finished.
        Usage: This is used is used to log the servers IP for reporting and locking down the scope.
        '''

        domainName = self.domainName # Get domain name from constructor.
        
        try:
            connectionLogger.logDebug('Calling getServerIP function - socket.gethostbyname(domainName)')
            serverIP = socket.gethostbyname(domainName)

        except socket.timeout as exceptionMsg:
            connectionLogger.logError('Calling getServerIP() - Server timeout.' + exceptionMsg)

        except socket.gaierror as exceptionMsg:
            connectionLogger.logError('Calling getServerIP() - Server not resolved.' + exceptionMsg)
        
        except socket.error as exceptionMsg:
            connectionLogger.logCritical('-- Exiting System --')
            connectionLogger.logError('Calling getServerIP() - Server could not connect.' + exceptionMsg)

        return serverIP
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------
    def setConnectionTimeout(self,timeout):
        '''
        Description: This function set the connection timeout.
        Status: Finished.
        Usage: This is used is used to log the servers IP for reporting and locking down the scope.
        '''
        socket.setdefaulttimeout(timeout)
