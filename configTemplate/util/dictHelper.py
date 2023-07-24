
def getParentXpath(xpath : str) -> str:

    if (type(xpath)):

        pathParts = xpath.split('[')

        pathPartsLength = len(pathParts)

        if (pathPartsLength <= 1):
            return None
        elif (pathPartsLength == 2):
            return pathParts[0]
        else:
            return '['.join(pathParts[:-1])
        
def joinChildToXpath(parentXpath : str, childIndex : str | int) -> str:

    if (type(childIndex) == str):
        return parentXpath + '["%s"]' % childIndex
    elif (type(childIndex == int)):
        return parentXpath + '[%d]' % childIndex
    
    raise Exception('Unsupported childIndex type of %s' % (str(type(childIndex))))