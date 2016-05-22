#####################################################################################################
#####################################################################################################
## Created on Sep 14, 2013
## @author: Gerasimos Kassaras
## E-mail: g.kassaras@gmail.com
## Nickname: Lamehacker Free Industries
## 
## Comment: This class is used to check typical web server security flag considerations. 
#######################################################################################################
#######################################################################################################

from bs4 import BeautifulSoup

import ConnectionManager.HttpHandler
import URLManager.URLAnalyzer
import LogManager.LogHandler

import re

httpValidator = LogManager.LogHandler.loggingHandler()# logs info,warning,error,critical,debug events.

class browserSecurityValidator:
        '''
        Description: This class is going to be used to test for security flags.
        Status: In progress.
        Usage: This class is used to implement all standard vulnerabilities in the web server flags.
        '''
        
        def __init__(self,domain,port):
            '''
            Description: This initializes the http flag tester.
            Status: In progress.
            Usage: This is used to test web server for proper configuration for the flags.
            '''
            self.port = port
            self.domain = domain
            
            self.httpOnlyFlag  = False
            self.secureFlag = False
            self.xXSSProtectionFlag = False
            self.xFrameOptionsFlag = False
            self.xContentTypeOptionsFlag = False
            self.xContentSecurityPolicyFlag = False
            self.xWebKitCSP = False
            self.cacheControlFlag = False
            self.pragmaFlag = False
            self.httpEquiv = False
            
             
            
            httpValidator.logInfo("---< Package: PassiveScanner - Module: browserSecurityValidator Class: browserSecurityValidator Initiated >---")
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------
        def getServerBanner(self,queryString):# Gets a query string and returns server banner.
            '''
            Description: This function iterates through the http/https header fields and returns the server field value.
            Status: Finished.
            Usage: This is used to identify if the server vulnerable based on the version, also going to be used for populating the report with the info of the server banner.
            '''
            
            webServer = ConnectionManager.HttpHandler.httpHandler(self.domain,self.port)
            webServer.getHttpGETResponse(queryString)
            headers  = webServer.httpGETResponseHeaders
            
            #Logging for banner grabber.
            httpValidator.logDebug(' -- Module browserSecurityValidator - Extracting Server Banner Event --')
            
            for headerField in range(len(headers)):
                if re.search('server',headers[headerField][0], re.IGNORECASE):
                    return headers[headerField][1]
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------
        def getAllowedMethods(self,queryString):# Gets a query string and returns server banner.
            '''
            Description: This function iterates through the http/https header fields and returns the server field value.
            Status: Finished.
            Usage: This is used to identify if the server vulnerable based on the version, also going to be used for populating the report with the info of the server banner.
            '''
            
            webServer = ConnectionManager.HttpHandler.httpHandler(self.domain,self.port)
            webServer.getHttpGETResponse(queryString)
            headers  = webServer.httpGETResponseHeaders
            
            
            #Logging for banner grabber.
            httpValidator.logDebug(' -- Module browserSecurityValidator - Extracting Server Banner Event --')
            
            for headerField in range(len(headers)):
                if re.search('server',headers[headerField][0], re.IGNORECASE):
                    return headers[headerField][1]
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------                
        def httpFlagValidator(self,queryString):
            '''
            Description: This function iterates through the http/https header fields and checks for the proper security flags.
            Status: In.
            Usage: This is used to identify if the server makes use of the httpOnly flag report that in the report generator module.
            '''
            
            webServer = ConnectionManager.HttpHandler.httpHandler(self.domain,self.port)
            webServer.getHttpGETResponse(queryString)
            rawHtml  = webServer.httpGETResponseRawHtml
            headers  = webServer.httpGETResponseHeaders
            
            for headerField in range(len(headers)):
                '''
                Description: This part of the code iterates through the http/https header fields and checks if the HttpOnly flag is set.
                Status: Finished (might have to come back and revisit).
                Usage: This is used to identify if the server makes use of the httpOnly flag report that in the report generator module.
                '''                
                if re.search('Set-Cookie',headers[headerField][0], re.IGNORECASE): # Test for HttpOnly flag.
                    if re.search(r'httpOnly',headers[headerField][1], re.IGNORECASE): 
                        self.httpOnlyFlag = True
                        
                        #Logging for httpOnly grabber.
                        httpValidator.logDebug(' -- Module browserSecurityValidator httpOnly flag: Found --')

            for headerField in range(len(headers)):
                '''
                Description: This part of the code iterates through the http/https header fields and checks if the secure flag is set, checks only the first cookie.
                Status: Finished (might have to come back and revisit).
                Usage: This is used to identify if the server makes use of the secure flag and report that in the report generator module.
                '''
                if re.search('Set-Cookie',headers[headerField][0], re.IGNORECASE): # Test Secure flag.
                    if re.search(r'secure',headers[headerField][1], re.IGNORECASE):
                        print headers[headerField][0]
                        self.secureFlag = True

                        #Logging for secure grabber.
                        httpValidator.logDebug(' -- Module httpValidator Secure flag: Found --')
               
                '''
                Description: This part of the code iterates through the http header fields and checks if the X-Frame-Options flag is set.
                Status: Finished (might have to come back and revisit).
                Usage: This is used to identify if the server makes use of the X-Frame-Options flag with SAMEORIGIN or DENY or ALLOW-FROM policies and report that in the report generator module.
                '''
                        
            for headerField in range(len(headers)): 
                if re.search('X-Frame-Options',headers[headerField][0], re.IGNORECASE):# Test for X-Frame-Options flag.
                    if re.search(r'(SAMEORIGIN)|(DENY)|(ALLOW-FROM)',headers[headerField][1], re.IGNORECASE):
                        self.xFrameOptionsFlag = True

                        #Logging for secure grabber.
                        httpValidator.logDebug(' -- Module httpValidator X-Frame-Options flag: Found --')

                '''
                Description: This part of the code iterates through the http/https header fields and checks if the X-XSS-Protection flag exists and is not set to 0.
                Status: Finished (might have to come back and revisit).
                Usage: This is used to identify if the server makes use of the X-XSS-Protection flag and is not set to 0 and report that in the report generator module.
                '''
                        
            for headerField in range(len(headers)):
                if re.search('x-xss-protection',headers[headerField][0], re.IGNORECASE):# Test for X-XSS-Protection flag.
                    if re.search(r'1',headers[headerField][1], re.IGNORECASE):# X-XSS-Protection is enabled.
                        self.xXSSProtectionFlag = True
 
                        #Logging for X-XSS-Protection grabber.
                        httpValidator.logDebug(' -- Module browserSecurityValidator X-XSS-Protection: Found set to 0 --')

                '''
                Description: This part of the code iterates through the http/https header fields and checks if the X-Content-Type-Options flag.
                Status: Finished (might have to come back and revisit).
                Usage: This is used to identify if the server makes use of the X-Content-Type-Options flag and report that in the report generator module.
                Reference: http://tools.ietf.org/html/rfc2616#section-14.9
                '''
                        
            for headerField in range(len(headers)):
                if re.search(r'X-Content-Type-Options',headers[headerField][0], re.IGNORECASE):
                    if re.search(r'nosniff',headers[headerField][1], re.IGNORECASE):
                        self.xContentTypeOptionsFlag = True

                        #Logging for X-Frame-Options grabber.
                        httpValidator.logDebug(' -- Module browserSecurityValidator X-Content-Type-Options: Found --')                        

            for headerField in range(len(headers)):
                if re.search(r'X-Content-Security-Policy',headers[headerField][0], re.IGNORECASE):
                    if re.search(r'(none)|(self)|(unsafe-inline)|(unsafe-eval)',headers[headerField][1], re.IGNORECASE):
                        self.xContentSecurityPolicyFlag = True

                        #Logging for X-Frame-Options grabber.
                        httpValidator.logDebug(' -- Module browserSecurityValidator X-Content-Security-Policy: Found --')

            for headerField in range(len(headers)):
                if re.search(r'X-WebKit-CSP',headers[headerField][0], re.IGNORECASE):
                    if re.search(r'(none)|(self)|(unsafe-inline)|(unsafe-eval)',headers[headerField][1], re.IGNORECASE):
                        self.xWebKitCSP = True

                        #Logging for X-WebKit-CSP grabber.
                        httpValidator.logDebug(' -- Module browserSecurityValidator X-WebKit-CSP: Found --') 

                '''
                Description: This function iterates through the http/https header fields and checks if the cache control flag is set to max-age=0 or no-store or no-cache.
                Status: In progress. TODO:
                Usage: This is used to identify if the server ssl cashed pages.
                Reference: http://tools.ietf.org/html/rfc2616#section-14.9
                '''
                        
            for headerField in range(len(headers)):                
                if re.search(r'cache-control',headers[headerField][0], re.IGNORECASE):
                    if re.search(r'(private)|(no-cache)|(no-store)',headers[headerField][1], re.IGNORECASE):
                        self.cacheControlFlag = True
                        
                        #Logging for X-WebKit-CSP grabber.
                        httpValidator.logDebug(' -- Module browserSecurityValidator cache-control: Found --') 

            for headerField in range(len(headers)):                        
                if re.search(r'pragma',headers[headerField][0], re.IGNORECASE):
                    if re.search(r'(private)|(no-cache)',headers[headerField][1], re.IGNORECASE):
                        self.pragmaFlag = True
                        
                        #Logging for X-WebKit-CSP grabber.
                        httpValidator.logDebug(' -- Module browserSecurityValidator pragma: Found --') 
              
            soup = BeautifulSoup(rawHtml)
            
            for tag in soup.findAll('meta', http-equiv=True) :
                print '----'+str(tag['content'])
                if re.search(r'(no-cache)|(no-store)|(must-revalidate)', tag['content'], re.IGNORECASE):
                    httpEquiv = True
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':
    
    tester = browserSecurityValidator('www.google.co.uk',80)
    tester.httpFlagValidator('/')
    print 'pragmaFlag: ' +str(tester.pragmaFlag)
    print 'httpOnlyFlag: ' +str(tester.httpOnlyFlag)
    print 'secureFlag: ' +str(tester.secureFlag)
    print 'cacheControlFlag: ' +str(tester.cacheControlFlag)
    print 'xContentSecurityPolicyFlag: ' +str(tester.xContentSecurityPolicyFlag)
    print 'xXSSProtectionFlag: ' +str(tester.xXSSProtectionFlag)
    print 'xFrameOptionsFlag: ' +str(tester.xFrameOptionsFlag)
    print 'getServerBanner: ' +str(tester.getServerBanner('/'))
    print 'httpEquiv: ' +str(tester.httpEquiv)