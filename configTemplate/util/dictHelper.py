from typing import Union

def getParentXpath(xpath : str) -> str:
    '''
    Return the parent xpath from "xpath"
    e.g. 
    xpath = $["root"]["foo"]["bar"]["var1"]

    Calling getParentXpath(xpath) will return $["root"]["foo"]["bar"]
    '''

    if (type(xpath) == str):

        pathParts = xpath.split('[')

        pathPartsLength = len(pathParts)

        if (pathPartsLength <= 1):
            return None
        elif (pathPartsLength == 2):
            return pathParts[0]
        else:
            return '['.join(pathParts[:-1])
        
    else:
        raise Exception('xpath is not a str')
    
def getParentXpathForKey(xpath : str, k : str) -> str:
    '''
    Return the parent xpath from "xpath" where k is first found.
    e.g. 
    xpath = $["root"]["foo"]["bar"]["var1"]

    Calling getParentXpathForKey(xpath, "foo") will return $["root"]["foo"]
    '''

    parentXpath = xpath
    while (parentXpath is not None):
        parentXpath = getParentXpath(parentXpath)

        if (parentXpath is not None and getChildKeyFromXpath(parentXpath) == k):
            return parentXpath

    return None
        
def getChildKeyFromXpath(xpath : str) -> Union[str, int]:
    '''
    Return the stripped child key name from the xpath.
    e.g.
    xpath = $["root"]["foo"]["bar"]["var1"]

    Calling getChildKeyFromXpath(xpath) will return 'var1'
    '''

    if (type(xpath) == str):

        pathParts = xpath.split('[')

        pathPartsLength = len(pathParts)

        if (pathPartsLength > 0):
            childPart = pathParts[-1].replace(']', '')
            if ('"' in childPart):
                return childPart.replace('"', '').strip()
            elif (childPart.isnumeric()):
                return int(childPart)
            elif (pathPartsLength == 1 and childPart == '$'):
                return '$'
            else:
                raise Exception('Unknown child type: %s' %  (str(type(childPart))))

        else:
            raise Exception('Unable to determine child key from xpath: %s' % (xpath))
        
    else:
        raise Exception('xpath is not a str')

        
def joinChildToXpath(parentXpath : str, childIndex : Union[str, int]) -> str:
    '''
    Returns an xpath by joing parentXpath with the childIndex.
    '''

    if (type(childIndex) == str):
        return parentXpath + '["%s"]' % childIndex
    elif (type(childIndex == int)):
        return parentXpath + '[%d]' % childIndex
    
    raise Exception('Unsupported childIndex type of %s' % (str(type(childIndex))))

def getDictFromFlatternedDict(flatternedDict : dict, xpathMatch : str) -> dict:
    '''
    Attempt to inflate a faltterned dict that are childern of xpathMatch.

    Note that inflating a flatterned dict cannot determine if the original was
    a list or a dictionary where indexes were integers.  Therefore all keys
    are assumed to be keys to a dict.
    '''

    matchedDict = {}
    
    if (xpathMatch in flatternedDict):
        if (not type(flatternedDict[xpathMatch]) == dict):
            raise Exception('xpath "%s" exists in flatternedDict and is not of type dict' % (xpathMatch))
        else:
            return flatternedDict[xpathMatch]
        
    for k in flatternedDict.keys():
        if (xpathMatch in k):
            matchedDict[getChildKeyFromXpath(k)] = flatternedDict[k]

    return matchedDict