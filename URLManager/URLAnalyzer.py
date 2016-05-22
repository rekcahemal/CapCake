#####################################################################################################
#####################################################################################################
## Created on Aug 29, 2013
## @author: Gerasimos Kassaras
## E-mail: g.kassaras@gmail.com
## Nickname: Lamehacker Free Industries
## 
## Comment: This class is used to handle all url parsing and should accept feed from the command line. 
#######################################################################################################
#######################################################################################################

from urlparse import urlparse

import re
import LogManager.LogHandler
from bs4 import UnicodeDammit

myurl1 = 'http://thesimplesitecompany.co.uk:80/wp-includes/js/jquery/jquery-migrate.min.js?ver=1.2.1'
myurl2 ='http://www.rbooks.co.uk/product.aspx?id=0385617313'
myurl3 = 'http://rhwidget.randomhouse.co.uk/flash-widget/widget_lg.do?isbn=9781849920247&menu=0&mode=1&cf=336699&cb=FFFFFF&newsletter=1'
myurl4 = 'http://thesimplesitecompany.co.uk:80'

urlLogger = LogManager.LogHandler.loggingHandler()# info,warning,error,critical,debug

class urlHandler:

    def __init__(self,url):# logs info,warning,error,critical,debug events.
        '''
        Description: This is the class constructor and is going to get a simple url as input and parse it based on RFC1738.
        Status: In Progress.
        Usage: This is going to be used by by the connection manager and the active/passive scanner to extract url variables.
        '''
        self.url = UnicodeDammit.detwingle(url, 'UTF-8')        
        self.defaultHttpsPort = 443
        self.defaultHttpPort = 80
        urlLogger.logInfo("--- Package: UrlManager - Module: UrlHandler Class: urlHandler Initiated ---")
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------
    def getUrlPath(self):# Gets no input, returns url path.
        '''
        Description: This function simply returns the url path.
        Status: Finished.
        Usage: This is going to be used by by the connection manager.
        '''
        
        return urlparse(self.url).path
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------
    def getUrlPathQueryWithoutParameters(self):# Gets no input, returns url path.
        '''
        Description: This function simply returns the url path.
        Status: Finished.
        Usage: This is going to be used by by the connection manager.
        '''
        
        return urlparse(self.url).path
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------
    def getUrlProtocol(self):# Gets no input, returns url protocol.
        '''
        Description: This function simply returns the url protocol e.g. http, https, ftp etc.
        Status: Finished.
        Usage: This is going to be used by the connection manager.
        '''
        
        return urlparse(self.url).scheme
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------
    def getUrlPort(self):# Gets no input, returns url port.
        '''
        Description: This function simply returns the url port.
        Status: Finished.
        Usage: This is going to be used by the connection manager.
        '''
        
        return urlparse(self.url).port
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------
    def getUrlHostname(self):# Gets no input, returns url hostname.
        '''
        Description: This function simply returns the url hostname.
        Status: Finished.
        Usage: This is going to be used by by the connection manager.
        '''
        
        return urlparse(self.url).hostname
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------
    def getUrlParametersValuePairsList(self):# Gets no input, returns a list of url parameters with values.
        '''
        Description: This function returns the url query parameter value parameter ditionary e.g. /<path>?<variable1=value1>&<varibale=value2>..... 
        The url structure based on rfcs is considered to have the following formats: 
            1) http ://<host>:<port>/<path>?<variable1=value1>&<varibale=value2>....
            2) http://<host>:<port>/<path>?<searchpart>
            3) https://<host>:<port>/<path>?<variable1=value1>&<varibale=value2>....
            4) https://<host>:<port>/<path>?<searchpart>
            5) http ://<host>:<port>/<path>#variable....
            6) https://<host>:<port>/<path>#variable....
            7) http ://<host>:<port>/<path>/<variable1=value>#<variable>....
            8) https://<host>:<port>/<path>/<variable1=value>#<variable>....
        Status: In Progress.
        Usage: This is going to be used other modules to identify vulnerabilities.
        Reference1: http://www.w3.org/Addressing/URL/url-spec.txt
        Reference2: http://www.ietf.org/rfc/rfc1738.txt
        Reference3: http://tools.ietf.org/html/rfc3986
        Reference4: http://en.wikipedia.org/wiki/Uniform_resource_locator
        '''
        
        urlList = self.url.split('?') # Split the url using the question mark.
        
        if re.search('\?',self.url):
            for urlToken in range(len(urlList)):
                if re.search('\=',urlList[urlToken]):
                    parameterValuePairList = urlList[urlToken]
            
            return parameterValuePairList.split('&')
        
        else:
            return []
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------
    def getUrlQueryString(self):# Gets no input, returns url query string.
        '''
        Description: This function returns the url query parameter value pair list e.g. /<path>?<variable1=value1>&<varibale=value2>..... 
        The url structure based on rfcs is considered to have the following formats: 
            1) http ://<host>:<port>/<path>?<variable1=value1>&<varibale=value2>....
            2) http://<host>:<port>/<path>?<searchpart>
            3) https://<host>:<port>/<path>?<variable1=value1>&<varibale=value2>....
            4) https://<host>:<port>/<path>?<searchpart>
            5) http ://<host>:<port>/<path>#variable....
            6) https://<host>:<port>/<path>#variable....
            7) http ://<host>:<port>/<path>/<variable1=value>#<variable>....
            8) https://<host>:<port>/<path>/<variable1=value>#<variable>....
        Status: In Progress.
        Usage: This is going to be used other modules to identify vulnerabilities.
        Reference1: http://www.w3.org/Addressing/URL/url-spec.txt
        Reference2: http://www.ietf.org/rfc/rfc1738.txt
        Reference3: http://tools.ietf.org/html/rfc3986
        Reference4: http://en.wikipedia.org/wiki/Uniform_resource_locator
        '''
        urlList = self.url.split('?') # Split the url using the question mark.
        
        path  = urlparse(self.url).path
        
        if re.search('\?',self.url):# Checks if the url contains any variables.
            for urlToken in range(len(urlList)):
                if re.search('\=',urlList[urlToken]):# Searches if it contains pairs of variables and values.
                    return path+'?'+urlList[urlToken] # Returns query string with variables.
        
        elif re.findall(r'/$', path, re.I):
            return path

        else:
            return path+'/'
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------
    def getUrlHostnameWithPort(self):# Gets no input, returns url netloc.
        '''
        Description: This function simply returns the url hostname port.
        Status: Finished.
        Usage: This is going to be used by by the connection manager.
        '''
        
        return urlparse(self.url).netloc
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------
    def getDefaultHttpPort(self):
        '''
        Description: This function simply returns the default http port 80.
        Status: Finished.
        Usage: This is going to be used by by the connection manager.
        '''
        
        return self.defaultHttpPort
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------
    def getDefaultHttpsPort(self):
        '''
        Description: This function simply returns the current https port 443.
        Status: Finished.
        Usage: This is going to be used by by the connection manager.
        '''
        
        return self.defaultHttpsPort
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------
    def usesHttp(self):
        '''
        Description: This function simply returns true if the url contains the protocol http and false if not.
        Status: Finished.
        Usage: This is going to be used by by the connection manager/html parser.
        '''
        
        if urlparse(self.url).scheme == 'http':
            return True
        
        else:
            return False
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------
    def usesHttps(self):
        '''
        Description: This function simply returns true if the url contains the protocol https and false if not.
        Status: Finished.
        Usage: This is going to be used by by the connection manager/html parser.
        '''
        
        if urlparse(self.url).scheme == 'https':
            return True
        
        else:
            return False
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------
    def hasUrlPort(self):
        '''
        Description: This function simply returns true if the url contains port information and false if not.
        Status: Finished.
        Usage: This is going to be used by by the connection manager/html parser.
        '''
        
        if urlparse(self.url).port:
            return True
        
        else:
            return False
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------
    def hasUrlProtocol(self):
        '''
        Description: This function simply returns true if the url contains protocol information and false if not.
        Status: Finished.
        Usage: This is going to be used by by the connection manager/parser.
        '''
        
        if urlparse(self.url).scheme: # If string empty then return false else true.  
            return True
        
        else:
            return False

'''
Used only for testing are going to remove later on.
'''
if __name__ == '__main__':
    
    myUrl = urlHandler(myurl4)
    print 'url :'+myurl4
    print 'getUrlQueryString: '+str(myUrl.getUrlQueryString())
    print 'getUrlHostnameWithPort: '+str(myUrl.getUrlHostnameWithPort())
    print 'getUrlParametersValuePairsList: '+str(myUrl.getUrlParametersValuePairsList())
    print 'getUrlPathQueryWithoutParameters: '+str(myUrl.getUrlPathQueryWithoutParameters())