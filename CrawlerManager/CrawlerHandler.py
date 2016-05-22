#####################################################################################################
#####################################################################################################
## Created on Aug 16, 2013
## 
## @author: Gerasimos Kassaras
## E-mail: g.kassaras@gmail.com
## Nickname: Lamehacker Free Industries
## 
## Conventions used in this coding style:
## Variable Naming Convention: urlSet - Is a set containing a set with url's
## Variable Naming Convention: cleanSet - Is a set that removes certain urls based on some conditions.
## Variable Naming Convention: subUrlSet - Is a sub set of a urlSet.
## Variable Naming Convention: urlList - Is a list containing a set with unfiltered url's
## Variable Naming Convention: cleanList - Is a list that removes certain urls based on some conditions.
## Variable Naming Convention: subUrlList - Is a sub set of a urlSet.
## TODO Naming Convention: The TODO Naming Convention is TODO: 
## Comments: Naming conventions are used are valid for every module within webshark. 
#######################################################################################################
#######################################################################################################

from bs4 import BeautifulSoup
import ConnectionManager.HttpHandler
import URLManager.URLAnalyzer
import Utilities.ListUtility
import LogManager.LogHandler
import re

parserLogger = LogManager.LogHandler.loggingHandler()# logs info,warning,error,critical,debug events.

class crawlerHandler:
    
    def __init__(self,startUrl):

        self.startUrl = startUrl 
        baseUrlObj = URLManager.URLAnalyzer.urlHandler(self.startUrl)# This object is used to manage the start url.
        self.targetLinks = [] # Is going to be used to keep target fetched links.
        self.allLinks = []# Is going to be used to keep all identified links.
        self.multipleURLsWithAttributes = []
        self.baseUrlObj = baseUrlObj
        self.domain = baseUrlObj.getUrlHostname() # Populated by command line or GUI
        
        parserLogger.logInfo("Package: CrawlerManager - Module: CrawlerHandler Class: crawlerHandler Initiated with base url")
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------
    def parseUrlsInfo(self,rawHtml,urlQueryToParse) : # Takes as an input a string and returns a list
        '''
        Description: This function is used to collect all urls from a single page and return a url list.
        Status: In progress.
        Usage: Is going to be used to collect html comments, JavaScript comments and email addresses.
        '''
        
        loadHtml = rawHtml # Load raw html from raw https/http responses.
        soup = BeautifulSoup(loadHtml)
        singleURLWithAttributes = dict([('urlQuery',''),('htmlComments',[]), ('javaScriptComments',[]), ('emailAddresses',[]),('urlVariables',[]),('sessionValue',[])])
        singleURLWithAttributes['urlQuery'] = urlQueryToParse
        urlList = []

        for tag in soup.findAll('link', href=True) : # Checks for links within the link tag e.g.<link rel="canonical" href="http://example.com/" />
            if re.search(r'(^http://)|(^https://)|(^/)|(^../)', tag['href'], re.IGNORECASE):
                urlList.append(tag['href'])

        for tag in soup.findAll('a', href=True) :# Checks for links within the a tag e.g. <a href="http://exmple.com/packages/"</a>
            if re.search(r'(^http://)|(^https://)|(^/)|(^../)', tag['href'], re.IGNORECASE):
                urlList.append(tag['href'])

        for tag in soup.findAll('meta', content=True) :# Checks for links within the content tag e.g.  <meta property="og:video" content="http://example.com/v/w0?version=3;autohide=1">
            if re.search(r'(^http://)|(^https://)|(^/)|(^../)', tag['content'], re.IGNORECASE): # Checks for links that start with http or https.
                urlList.append(tag['content'])

        for tag in soup.findAll('script', src=True) :# Checks for links within the script tag e.g. <script type='text/javascript' src="http://example.com/wp-includes/js/jquery/jquery.js"></script>
            if re.search(r'(^http://)|(^https://)|(^/)|(^../)', tag['src'], re.IGNORECASE):
                urlList.append(tag['src'])
                
        for tag in soup.findAll('area', href=True) :# Checks for links within the script tag e.g. <area href="http://www.example.com/product.aspx?id=0385617321" target="_blank" alt="Buy Now" />

            if re.search(r'(^http://)|(^https://)|(^/)|(^../)', tag['href'], re.IGNORECASE):
                urlList.append(tag['href'])

        for tag in soup.findAll('script', href=True) :# Checks for links within the script tag e.g. <div href="http://www.example.com/product.aspx?id=0385617321" target="_blank" alt="Buy Now" />

            if re.search(r'(^http://)|(^https://)|(^/)|(^../)', tag['href'], re.IGNORECASE):
                urlList.append(tag['href'])
        
        for tag in soup.findAll('frame', src=True) :# Checks for links within the script tag e.g. <div href="http://www.example.com/product.aspx?id=0385617321" target="_blank" alt="Buy Now" />

            if re.search(r'(^http://)|(^https://)|(^/)|(^../)', tag['src'], re.IGNORECASE):
                urlList.append(tag['src'])
                
        for tag in soup.findAll('frame', href=True) :# Checks for links within the script tag e.g. <div href="http://www.example.com/product.aspx?id=0385617321" target="_blank" alt="Buy Now" />

            if re.search(r'(^http://)|(^https://)|(^/)|(^../)', tag['src'], re.IGNORECASE):
                urlList.append(tag['href'])

############################################################## Generic Information Collectors #################################################################################

        for htmlComment in soup(text=re.compile(r'\<![ \r\n\t]*(--([^\-]|[\r\n]|-[^\-])*--[ \r\n\t]*)\>',re.DOTALL)):# Match all html comments and extract them.
            
            (singleURLWithAttributes['htmlComments']).append(htmlComment)
            print '--------------'
            print singleURLWithAttributes['urlQuery']
            print singleURLWithAttributes['htmlComments']
            
        for javascriptComment in soup(text=re.compile(r'/((?:\/\*(?:[^*]|(?:\*+[^*\/]))*\*+\/)|(?:\/\/.*))/',re.DOTALL)):# Match all comments starting with /* and ending in */ and extract them.
            
            (singleURLWithAttributes['javascriptComments']).append(javascriptComment)

            
        for emailAddresses in soup(text=re.compile(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', re.DOTALL)):# Match all email addresses.
            
            (singleURLWithAttributes['emailAddresses']).append(emailAddresses)


##############################################################################################################################################################################
        
        self.multipleURLsWithAttributes.append(singleURLWithAttributes)
        
        return urlList
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------
    def httpFetcher(self,urlList):# Takes as an input a list and returns a list - Also collect other info.
        '''
        Description: This function is used to as a fetcher for to collect urls, fetched from raw html.
        Status: In progress
        Usage: Is going to be used to collect per page all urls (the pages used to colect from the urls can be both SSL and none SSL).
        '''
        
        rawUrlList = [] # This is a none filtered list of urls collected
        rawHtml = '' # Used to collect all raw html.
        
        for url in urlList:
            urlObj = URLManager.URLAnalyzer.urlHandler(url) # Used to parse the url.

            if not url in self.targetLinks: # If the url is already fetched is not going to re-fetch.
                if urlObj.hasUrlProtocol():# This means that the url contains the http keyword.
                    if urlObj.usesHttp() and urlObj.hasUrlPort():# This link in this situation is not an internal link (e.g. a link starting with / or ../ or ./) and has only a path, that is why I am extracting again all info.
                        server = ConnectionManager.HttpHandler.httpHandler(self.domain,urlObj.getUrlPort()) # Initiate connection manager.
                        rawHtml = server.getHttpGETResponse(urlObj.getUrlQueryString()) # Fetch server HTML page.
                        rawUrlList.append(self.parseUrlsInfo(rawHtml,urlObj.getUrlQueryString())) # Fetch urls from each page.
                        self.targetLinks.append(url) # Record non visited links.
                        
                        # Logging functionality.
                        parserLogger.logDebug('Calling dataPuller function - urlObj.getUrlQueryString(): '+urlObj.getUrlQueryString())
                                              
                    elif urlObj.usesHttps() and urlObj.hasUrlPort():# This link in this situation is not an internal link (e.g. a link starting with / or ../ or ./) and has only a path, that is why I am extracting again all info.
                        server = ConnectionManager.HttpHandler.httpHandler(self.domain,urlObj.getUrlPort()) # Initiate connection manager.
                        rawHtml = server.getHttpsGETResponse(urlObj.getUrlQueryString()) # Fetch server HTML page.
                        rawUrlList.append(self.parseUrlsInfo(rawHtml,urlObj.getUrlQueryString())) # Fetch urls from each page.
                        self.targetLinks.append(url) # Record non visited links.
                        
                        # Logging functionality.
                        parserLogger.logDebug('Calling httpFetcher function - urlObj.getUrlQueryString(): '+urlObj.getUrlQueryString())
                        
                    elif urlObj.usesHttp() and not urlObj.hasUrlPort():# This link in this situation is not an internal link (e.g. a link starting with / or ../ or ./) and has only a path, that is why I am extracting again all info.
                        server = ConnectionManager.HttpHandler.httpHandler(self.domain,urlObj.getUrlPort()) # Initiate connection manager.
                        rawHtml = server.getHttpGETResponse(urlObj.getUrlQueryString()) # Fetch server HTML page.
                        rawUrlList.append(self.parseUrlsInfo(rawHtml,urlObj.getUrlQueryString())) # Fetch urls from each page.
                        self.targetLinks.append(url) # Record non visited links.
                        
                        # Logging functionality.
                        parserLogger.logDebug('Calling httpFetcher function - urlObj.getUrlQueryString(): '+str(urlObj.getUrlQueryString()))
                        
                    elif urlObj.usesHttps() and not urlObj.hasUrlPort():# This link in this situation is not an internal link (e.g. a link starting with / or ../ or ./) and has only a path, that is why I am extracting again all info.
                        server = ConnectionManager.HttpHandler.httpHandler(self.domain,urlObj.getUrlPort()) # Initiate connection manager.
                        rawHtml = server.getHttpsGETResponse(urlObj.getUrlQueryString()) # Fetch server HTML page.
                        rawUrlList.append(self.parseUrlsInfo(rawHtml,urlObj.getUrlQueryString())) # Fetch urls from each page.
                        self.targetLinks.append(url) # Record non visited links.
                        
                        # Logging functionality.
                        parserLogger.logDebug('Calling httpFetcher function - urlObj.getUrlQueryString(): '+urlObj.getUrlQueryString())
                        
                elif self.baseUrlObj.usesHttp():# The link in this situation is an internal link and has only a path, that is why I am using the start url.
                    server = ConnectionManager.HttpHandler.httpHandler(self.domain,urlObj.getDefaultHttpPort()) # Initiate connection manager.
                    rawHtml = server.getHttpGETResponse(urlObj.getUrlQueryString()) # Fetch server HTML page.
                    rawUrlList.append(self.parseUrlsInfo(rawHtml,urlObj.getUrlQueryString())) # Fetch urls from each page.
                    self.targetLinks.append(url) # Record non visited links.
                    
                    # Logging functionality.
                    parserLogger.logDebug('Calling httpFetcher function - urlObj.getUrlQueryString(): '+urlObj.getUrlQueryString())
                    
                elif self.baseUrlObj.usesHttps(): # The link in this situation is an internal link and has only a path, that is why I am using the start url.
                    server = ConnectionManager.HttpHandler.httpHandler(self.domain,urlObj.getDefaultHttpsPort())
                    rawHtml = server.getHttpsGETResponse(urlObj.getUrlQueryString()) # Fetch urls from each page.
                    rawUrlList.append(self.parseUrlsInfo(rawHtml,urlObj.getUrlQueryString())) # Fetch urls from each page.
                    self.targetLinks.append(url) # Record non visited links.
                    
                    # Logging functionality.
                    parserLogger.logDebug('Calling httpFetcher function - urlObj.getUrlQueryString(): '+urlObj.getUrlQueryString())
                        
        parserLogger.logInfo('Calling httpFetcher function result (rawList): '+str(rawUrlList))

        return rawUrlList
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------
    def removeNonHtmlLinks(self,urlList): # Takes as an input a list and returns a list.
        '''
        Description:This function extracts non html files from from the urls collected.
        Status: TODO: In progress
        Usage: e.g. Extract Windows Files from each URL , is going to be used to export certain types of files in folders
        ''' 
    
        rm = ['.ZIP','.JPG','.DMG','.MSI','.RAR','BZ2','TGZ','.CHM','.TAR','.EXE','.XZ','.DOC','.PDF','.PNG','.JPG','.TIFF','MAILTO','#','XPI','CRX'] #Add here all the urls you would like to remove from final url list
    
        cleanList = []
        tmp = urlList
    
        for fileSuffix in range(len(rm)):
            for element in range(len(tmp)):
                if re.search(rm[fileSuffix],urlList[element],re.IGNORECASE):
                    cleanList.append(urlList[element])
                    # Logging functionality
                    parserLogger.logDebug('Calling removeContent function - file ending element: '+urlList[element])
        
        parserLogger.logInfo('Calling removeContent function - result(cleanList): '+str(cleanList))
        return cleanList
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------
    def filterOut(self, urlList): # Takes as an input a list and returns a list.
        '''
        Description: This function filters out doubles and and non html content and keeps track of all visited links.
        Status: Finished.
        Usage: Is used to protect the html parser from crashing, analyzing the non html content, removing double urls and updating target links and all link state.
        '''
        
        listObj = Utilities.ListUtility.listUtilities()# Engage list utility tool for filtering collected urls.
        cleanList = urlList
        
        cleanList = listObj.flattenList(cleanList) # Target domain links.
        parserLogger.logInfo('Calling purify function results flattenList(cleanList): '+str(cleanList))
        cleanList = listObj.deduplicateLinks(cleanList) # Target domain links.
        parserLogger.logInfo('Calling purify function results deduplicateLinks(cleanList): '+str(cleanList))
        
        listObj.copyLinks(cleanList, self.allLinks) # Collect and non target domain links.
        parserLogger.logInfo('Calling purify function results copyLinks(cleanList,self.domain): '+str(self.allLinks))
        self.allLinks = listObj.deduplicateLinks(self.allLinks) # Target domain links.
        parserLogger.logInfo('Calling purify function results deduplicateLinks(self.allLinks,self.domain): '+str(self.allLinks))
        
        cleanList = self.restrictToTargetDomain(cleanList,self.domain) #  # Target domain links, restricting urls to main domain.
        parserLogger.logInfo('Calling purify function results restrictToTargetDomain(cleanList,self.domain): '+str(cleanList))
        cleanList = listObj.removeBadLinks(cleanList,self.removeNonHtmlLinks(cleanList)) # Clean up non html content.
        parserLogger.logInfo('Calling purify function results removeBadLinks(cleanList,removeNonHtmlLinks(cleanList)): '+str(cleanList))
    
        return cleanList
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------
    def singlePage(self,urlList): # Input is a list, output is a list
        '''
        Description: This function is used to fetch a single page urls.
        Status: Finished.
        Usage: Is used within the harvester to fetch for a single page the urls.
        '''

        urlList = self.httpFetcher(urlList)
        parserLogger.logDebug('Calling singlePage function after httpFetcher: '+str(urlList))
        urlList = self.filterOut(urlList)
        parserLogger.logDebug('Calling singlePage function after purify: '+str(urlList))
    
        return urlList
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------
    def restrictToTargetDomain(self,urlList,domain) : # Takes as an input a list and returns a list.
        '''
        Description: This function transforms the collected urls so as to be use later on by httplib to collect more urls.
        Status: Finished.
        Comment: Might have to revisit.
        Usage: Restrict crawling to the start url.
        '''
        
        cleanList = []
        
        for url in range(len(urlList)):
            if re.search(r'(^/)|(^../)',urlList[url],re.IGNORECASE):# Search for inner urls.
                cleanList.append(urlList[url])
                
                parserLogger.logDebug('Calling restrictToScope function for internal urls: '+urlList[url])
    
            if re.search(self.domain,urlList[url],re.IGNORECASE):# Restrict url collection to same domain.
                cleanList.append(urlList[url])
                
                parserLogger.logDebug('Calling restrictToScope function for domain urls: '+urlList[url])
    
        return cleanList
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------
    def collectAllUrls(self):# Accepts the initial domain name as a url list.
        '''
        Description: This function is used to collect all urls from the given url (through the command line).
        Status: In Progress
        Usage: This is the main function within the crawler.
        '''

        urlList = []
        urlList.append(self.startUrl) # This is the base url for starting crawling.
        urlCollector = [] # Returns the collected urls and should be equal to the targetLinks list when this is function is going to terminate.
        nextPage = self.singlePage(urlList)# Gets the start urls (usual a the domain name).

        nextPageLinks = Utilities.ListUtility.listUtilities()# Used to manipulate the list.

        while True:
    
            nextPage = self.singlePage(nextPage)# httpFetcher the next page.)
            
            if nextPageLinks.containsNoLinks(nextPage):# If the targetLinks list contains the urlCollector links then the list shrinks to an empty list.
                break

            for eachLink in range(len(nextPage)):
                if not nextPageLinks.containsAllFetchedLinks(urlCollector,nextPage): # Check if the fetched urls is a subset of the collected links.
                    urlCollector.append(nextPage[eachLink])
    
            nextPage = urlCollector # Update next page with the collected urls from the previous page.

        return urlCollector
