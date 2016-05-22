#####################################################################################################
#####################################################################################################
## Created on Aug 29, 2013
## @author: Gerasimos Kassaras
## E-mail: g.kassaras@gmail.com
## Nickname: Lamehacker Free Industries
## 
## Comment: This class is used to export in plain txt files the 
#######################################################################################################
#######################################################################################################

from bs4 import BeautifulSoup
import bs4.dammit
from bs4.dammit import EntitySubstitution, UnicodeDammit
import LogManager.LogHandler

headers = [('x-powered-by', 'PHP/5.3.26'), ('transfer-encoding', 'chunked'), ('set-cookie', 'wc_session_cookie_87f666e4cdc669381b87c42cfa9344bf=FdN2CSwtLhKBw6D5BypBdOVycekqKDD5%7C%7C1379192522%7C%7C1379188922%7C%7Ca78964a464e48f83e8381f7e4f389845; expires=Sat, 14-Sep-2013 21:02:02 GMT; path=/; httponly, woocommerce_items_in_cart=0; expires=Thu, 12-Sep-2013 20:02:02 GMT; path=/, woocommerce_cart_hash=0; expires=Thu, 12-Sep-2013 20:02:02 GMT; path=/'), ('expires', 'Thu, 12 Sep 2013 22:02:02 GMT'), ('vary', 'Accept-Encoding,User-Agent'), ('keep-alive', 'timeout=20'), ('server', 'nginx/1.4.2'), ('connection', 'keep-alive'), ('link', '<http://wp.me/37q4W>; rel=shortlink'), ('cache-control', 'max-age=3600'), ('date', 'Thu, 12 Sep 2013 21:02:02 GMT'), ('content-type', 'text/html; charset=UTF-8'), ('x-pingback', 'http://thesimplesitecompany.co.uk/xmlrpc.php')]


exportFeedLogger = LogManager.LogHandler.loggingHandler()# logs info,warning,error,critical,debug events.

class exportFeed:
    '''
    Description: This class is used to export feed in plain text.
    Status: In progress.
    Usage: Is used within the crawler to export feeds.
    '''

    def __init__(self):
        exportFeedLogger.logInfo("Package: ExportManager - Module: ExportHandler Class: exportFeed Initiated with base url")

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------
    def exportUrlFeeder(self, filename,urlList):# Takes as an input a list and returns nothing.
        '''
        Description: This function is used to export the urls into a flat file.
        Status: In progress - Should be moved to a separate package.
        Usage: Is used within the harvest functions as a url exporter.
        '''

        urlList  = sorted(urlList) # Sort urls so it can be more easy to read.
        fobj = open(filename,'wa')
        
        for link in range(len(urlList)):
            try:
                encodedUrl = UnicodeDammit.detwingle(urlList[link])
                encodedUrl.decode("utf8")
                fobj.write(encodedUrl) # Exports the urls in a file.Re move function-
                fobj.write('\n')
            except:
                exportFeedLogger.logError("Unexpected error while open output file in exportUrlFeeder")
                pass
        
        fobj.flush() # Flush IO buffer.
        fobj.close()# Close file.
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------
    def exportContentFeeder(self, filename,rawHtmlList):# Takes as an input a list and returns nothing.
        '''
        Description: This function is used to export the whole target domain html into a flat file.
        Status: In finished
        Usage: Is used within the feed functions as a html exporter.
        '''
        
        fobj = open(filename,'wa')
        
        for page in range(len(rawHtmlList)):
            try:
                soup = BeautifulSoup(rawHtmlList[page])
                fobj.write(soup.prettify())
                fobj.write('\n')
                fobj.write('-----------------------------------------------------------------------------------------------------------')
                fobj.write('\n')
            except:
                exportFeedLogger.logError("Unexpected error while open output file in exportContentFeeder")
                pass
            
        fobj.flush() # Flush IO buffer.
        fobj.close()# Close file.
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------
    def exportHeadersFeeder(self, filename,headerList):# Takes as an input a list of tuples and returns nothing.
        '''
        Description: This function is used to export the http/https  headers into a flat file.
        Status: Finished
        Usage: Is used within the harvest functions as a http/https header exporter for being used with active & passive scanner.
        '''
        
        fobj = open(filename,'wa')
        
        for headerElement in range(len(headerList)):
            singleHeader = headerList[headerElement]
            try:
                for header in range(len(singleHeader)):
                    fobj.write(str(singleHeader[header]))
                    fobj.write('\n')
                    fobj.write('-----------------------------------------------------------------------------------------------------------')
                    fobj.write('\n')
            except:
                exportFeedLogger.logError("Unexpected error while open output file in exportHeadersFeeder")
                pass
            
        fobj.flush() # Flush IO buffer.
        fobj.close()# Close file.

    def exportHeadersFeeder1(self, filename,headerList):# Takes as an input a list of tuples and returns nothing.
        '''
        Description: This function is used to export the http/https  headers into a flat file.
        Status: Finished
        Usage: Is used within the harvest functions as a http/https header exporter for being used with active & passive scanner.
        '''
        
        for headerElement in range(len(headerList)):
            try:
                print str(headerList[headerElement][0])+' : '+str(headerList[headerElement][1])
            except:
                exportFeedLogger.logError("Unexpected error while open output file in exportHeadersFeeder")
                pass

if __name__ == '__main__':
     feeder1 = exportFeed()
     feeder1.exportHeadersFeeder1('out',headers)
    