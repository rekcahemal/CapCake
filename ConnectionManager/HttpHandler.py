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

import httplib
import urllib
import LogManager.LogHandler
import ConnectionManager.ConnectionHandler

httpLogger = LogManager.LogHandler.loggingHandler()# logs info,warning,error,critical,debug events.

class httpHandler(ConnectionManager.ConnectionHandler.connnectionHandler):
    '''
    Description: This initializes the http/https handler class.
    Status: In progress.
    Usage: This is used to initialize the all needed information to connect to the http/https server.
    '''
    
    def __init__(self,domainName,port):
        '''
        Description: This initializes the http/https handler class.
        Status: In progress.
        Usage: This is used to initialize the all needed information to connect to the server.
        '''
        
        self.domainName = domainName # This value is populated from the each inserted url.
        self.port = port # This value is populated from the each inserted url.
        
        # These value is populated from the each get http response.
        self.httpGETResponseHeaders = '' # Returns a tuple of headers
        self.httpGETResponseStatus = '' # Status code returned by server.
        self.httpGETResponseHttpProtocolVersion = ''
        self.httpGETResponseHttpReason = '' # Reason phrase returned by server.
        self.httpGETResponseRawHtml = '' # Returns back the raw html body

        # These values are populated from the each http post response.
        self.httpPOSTResponseHeaders = ''
        self.httpPOSTResponseStatus = '' # Status code returned by server.
        self.httpPOSTResponseProtocolVersion = ''
        self.httpPOSTResponseReason = '' # Reason phrase returned by server.
        self.httpPOSTResponseRawHtml = '' # Returns back the raw html body

        # These values are populated from the each https get response.
        self.httpsGETResponseHeaders = ''
        self.httpsGETResponseStatus = '' # Status code returned by server.
        self.httpsGETResponseProtocolVersion = ''
        self.httpsGETResponseReason = '' # Reason phrase returned by server.
        self.httpsGETResponseRawHtml = '' # Returns back the raw html body

        # These values are populated from the each https post response.
        self.httpsPOSTResponseHeaders = ''
        self.httpsPOSTResponseStatus = '' # Status code returned by server.
        self.httpsPOSTResponseProtocolVersion = ''
        self.httpsPOSTResponseReason = '' # Reason phrase returned by server.
        self.httpsPOSTResponseRawHtml = '' # Returns back the raw html body
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------
    def getHttpGETResponse(self, urlPath): # Takes as an input a string (url path) and returns a string (raw html)
        '''
        Description: This function is used start getting http get requests.
        Status: Finished.
        Usage: Fetching the html from the server. 
        '''
        
        domainName = self.domainName
        port = self.port  

        try:
            httpLogger.logDebug('Calling getHttpGETResponse function - Fetching URL path: '+str(urlPath))
            conn = httplib.HTTPConnection(domainName,port)
            conn.request("GET",urlPath)
            response = conn.getresponse() # Collect http response body
            # Harvesting information about the connection.
            self.httpGETResponseHeaders = response.getheaders() # Returns a tuple of headers
            self.httpGETResponseStatus = response.status # Status code returned by server.
            self.httpGETResponseProtocolVersion = response.version
            self.httpGETResponseReason = response.reason # Reason phrase returned by server.
            self.httpGETResponseRawHtml = response.read()
            
        except httplib.error:
            httpLogger.logError('Exception generated in Connection Manager Package - getHttpGETResponse')
            pass
    
        return self.httpGETResponseRawHtml
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------
    def getHttpsGETResponse(self, urlPath): # Takes as an input a string and returns a string 
        '''
        Description: This function is used start getting https get requests.
        Status: Finished.
        Usage: Fetching the html from the server. 
        '''

        domainName = self.domainName
        port = self.port 

        try:
            httpLogger.logDebug('Calling getHttpsGETResponse function - Fetching URL path: '+urlPath)
            conn = httplib.HTTPSConnection(domainName,port)
            conn.request("GET",urlPath)
            response = conn.getresponse() # Collect http response body.
            
            # Harvesting information about the connection.
            self.httpsGETResponseHeaders = response.getheaders() # Returns a tuple of headers
            self.httpsGETResponseStatus = response.status # Status code returned by server.
            self.httpsGETResponseProtocolVersion = response.version
            self.httpsGETResponseReason = response.reason # Reason phrase returned by server.

        except httplib.error as exceptionMsg:
            httpLogger.logError('Function getHttpGETResponse(self, urlPath)  caused an exception'+exceptionMsg)
            pass
    
        return response.read()
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------
    def getHttpOPTIONSResponse(self): # Takes as an input a string and returns a string.
        '''
        Description: This function is used start getting http options requests.
        Status: Finished.
        Usage: Fetching the html from the server. 
        '''

        domainName = self.domainName
        port = self.port 

        try:
            httpLogger.logDebug('Calling getHttpOPTIONSResponse function - Fetching URL path: /')
            conn = httplib.HTTPConnection(domainName,port)
            conn.request('OPTIONS','/')
            response = conn.getresponse() # Collect http response body
    
        except httplib.error as exceptionMsg:
            httpLogger.logError('Function getHttpOPTIONSResponse(self) generated exception: '+exceptionMsg)
            pass
    
        return response.read()
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------
    def getHttpsOPTIONSResponse(self): # Takes as an input a string and returns a string 
        '''
        Description: This function is used start getting https options requests.
        Status: Finished.
        Usage: Fetching the html from the server. 
        '''

        domainName = self.domainName
        port = self.port 

        try:
            httpLogger.logDebug('Calling getHttpsOPTIONSResponse function - Fetching URL path: /')
            conn = httplib.HTTPSConnection(domainName,port)
            conn.request('OPTIONS','/')
            response = conn.getheader('allow')
    
        except httplib.error as exceptionMsg:
            httpLogger.logError('Function getHttpsOPTIONSResponse(self) generated exception: '+exceptionMsg)
            pass
    
        return response
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------
    def getHttpHEADResponse(self, urlPath): # Takes as an input a string and returns a string
        '''
        Description: This function is used start sending http head requests.
        Status: Finished.
        Usage: Fetching the html from the server. 
        '''

        domainName = self.domainName
        port = self.port 

        try:
            httpLogger.logDebug('Calling getHttpHEADResponse function - Fetching URL path: '+urlPath)
            conn = httplib.HTTPConnection(domainName,port)
            conn.request("HEAD",urlPath)
            response = conn.getresponse() # Collect http response body
    
        except httplib.error as exceptionMsg:
            httpLogger.logError('Function getHttpHEADResponse(self, urlPath) generated exception: '+exceptionMsg)
            pass
    
        return response.read()
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------
    def getHttpsHEADResponse(self, urlPath): # Takes as an input a string and returns a string 
        '''
        Description: This function is used start getting https head requests.
        Status: Finished.
        Usage: Fetching the html from the server. 
        '''

        domainName = self.domainName
        port = self.port 

        try:
            httpLogger.logDebug('Calling getHttpsHEADResponse function - Fetching URL path: '+urlPath)
            conn = httplib.HTTPSConnection(domainName,port)
            conn.request("HEAD",urlPath)
            response = conn.getresponse() # Collect http response body.
            
        except httplib.error as exceptionMsg:
            httpLogger.logError('Function getHttpsHEADResponse(self, urlPath) generated exception: '+exceptionMsg)
            pass
    
        return response.read()
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------
    def getHttpPOSTResponse(self, params,headers): # Takes as an input a string and returns a string.
        '''
        Description: This function is used start getting http post requests.
        Status: Finished.
        Usage: Fetching the html from the server. 
        ''' 

        parameters = urllib.urlencode({'@number': 12524, '@type': 'issue', '@action': 'show'})#TODO:
        headers = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain"}#TODO:
        domainName = self.domainName
        port = self.port 

        try:
            httpLogger.logDebug('Calling getHttpPOSTResponse function - sending POST parameters: '+str(parameters))
            conn = httplib.HTTPConnection(domainName,port)
            conn.request("POST",parameters,headers)
            response = conn.getresponse() # Collect http response body
    
        except httplib.error as exceptionMsg:
            httpLogger.logError('Function getHttpPOSTResponse(self, params,headers) generated exception: '+exceptionMsg)
            pass
    
        return response.read()
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------
    def getHttpsPOSTResponse(self, params,headers): # Takes as an input a string and returns a string 
        '''
        Description: This function is used start getting https post requests.
        Status: Finished.
        Usage: Fetching the html from the server. 
        '''

        parameters = urllib.urlencode({'@number': 12524, '@type': 'issue', '@action': 'show'})#TODO:
        headers = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain"}#TODO:
        domainName = self.domainName
        port = self.port 

        try:
            httpLogger.logDebug('Calling getHttpsPOSTResponse function - sending POST parameters: '+str(parameters))
            conn = httplib.HTTPSConnection(domainName,port)
            conn.request("POST",parameters,headers)
            response = conn.getresponse() # Collect http response body
    
        except httplib.error as exceptionMsg:
            httpLogger.logError('Function getHttpsPOSTResponse(self, params,headers) generated exception: '+exceptionMsg)
            pass
    
        return response.read()


if __name__ == '__main__':
     ser = httpHandler('thesimplesitecompany.co.uk',80)
     print ser.getHttpOPTIONSResponse()

    
