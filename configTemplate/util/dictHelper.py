from typing import Union

def getParentXpath(xpath : str) -> str:

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
        
def getChildKeyFromXpath(xpath : str) -> str:

    if (type(xpath) == str):

        pathParts = xpath.split('[')

        pathPartsLength = len(pathParts)

        if (pathPartsLength > 0):
            childPart = pathParts[-1].replace(']', '')
            if ('"' in childPart):
                return childPart.replace('"', '').strip()
            elif (childPart.isnumeric()):
                return int(childPart)
            else:
                raise Exception('Unknown child type: %s' %  (str(type(childPart))))

            return 
        else:
            raise Exception('Unable to determine child key from xpath: %s' % (xpath))
        
    else:
        raise Exception('xpath is not a str')

        
def joinChildToXpath(parentXpath : str, childIndex : Union[str, int]) -> str:

    if (type(childIndex) == str):
        return parentXpath + '["%s"]' % childIndex
    elif (type(childIndex == int)):
        return parentXpath + '[%d]' % childIndex
    
    raise Exception('Unsupported childIndex type of %s' % (str(type(childIndex))))

def getDictFromFlatternedDict(flatternedDict : dict, xpathMatch : str) -> dict:

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