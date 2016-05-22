
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

import itertools

class listUtilities:

    '''
    Description: This function receives a list with the collected urls and removes double urls.
    Status: Finished.
    Usage: Is used to avoid re-downloading the same urls and going through loops by the parser.
    '''
    def deduplicateLinks(self,urlList):# Takes as an input a list and returns a list.
        
        urlList = list(set(urlList))
        
        return urlList
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------
    def flattenList(self,urlList):# Takes as an input a list and returns a list.
        '''
        Description: This function is going to be used as a merger for the list returned from the parseHtml function.
        Status: Finished.
        Usage: Is used to prevent the url parser from crashing by converting a list of lists to a list of urls.
        '''
        
        while True:
            if any(isinstance(element, list) for element in urlList): # Checks through all list elements to find lists.
                ''' 
                Check if this is a list of lists of type [...[]...] or of type [...[],[],[]...].
                Examples lists that checks:
                    1.[['/about','/search','/help']]
                    2.[[['/about']]]
                    3.[['/about',['/search'],'/help']]
                '''
                urlList = list(itertools.chain(*urlList))
                ''' 
                Removes external brackets from a list of lists of type [...[]...] or of type [...[],[],[]...].
                Examples lists that alters:
                    1. Input:[['/about'],['/search'],['/help']] -> Output: ['/about','/search','/help']
                    2. Input:[[[[['/about']]]]] -> Output: ['/about']
                    3. Input:[['/about',['/search'],'/hp']] -> Output:['/about','/search','/','h','p'] - Breaks the parser - Should never occur. 
                '''
            else:
                break # Break the loop if this is not a list of lists.
        
        return urlList
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------
    def removeBadLinks(self, urlList,urlSublist): # Takes as an input a list and returns a list.
        '''
        Description: This function receives a list with the collected urls and subtracts a sublist of urls.
        Status: Finished.
        Usage: Is used to protect the html parser from crashing and help later on to analyze the non html content.
        '''
        
        urlSet = set(urlList)
        urlSubset = set(urlSublist)
        clearSet = urlSet - urlSubset
        
        return list(clearSet) # Convert again to list.
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------
    def containsAllFetchedLinks(self,collectedUrlList,nextPageUrlList):# Takes as an input a list and returns true or false.
        '''
        Description: This function is used to find if the next page contains the same links with the previous page.
        Status: Finished
        Usage: Is used within the harvest functions as a termination condition.
        '''
        
        collectedUrlSet = set(collectedUrlList)
        nextPageUrlSet = set(nextPageUrlList)
        
        if nextPageUrlSet.issubset(collectedUrlSet):
            return True
        else:
            return False
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------
    def containsNoLinks(self,page):# Takes as an input a list and returns true or false.
        '''
        Description: This function is used to find if a link list is empty.
        Status: Finished
        Usage: Is used within the harvest functions as a termination condition.
        '''
        
        if page == []:
            return True
        else:
            return False
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------
    def copyLinks(self,urlList,copiedList):# Takes as an input a list and returns true or false.
        '''
        Description: This function is used to copy all links identified so far.
        Status: Finished
        Usage: Is used within the collector to extract interesting links from the target domain.
        '''
        
        for eachUrl in range(len(urlList)):# De-dublicate all url list for furher analysis.
            copiedList.append(urlList[eachUrl])
            
        return False