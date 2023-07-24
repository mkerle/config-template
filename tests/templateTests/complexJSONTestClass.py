from configTemplate.util import dictHelper

class DeviceSettings(object):

    def __init__(self, name):

        self.portIdentifierXpath = '$_var_portIdentifier'

        self.physicalPort = 'port1'

        self.name = name


    def getInterfaceTemplateSettings(self, xpath : str, propertyName : str, flatternedTemplate : dict) -> any:

        parentXpath = dictHelper.getParentXpath(xpath)

        interfaceSettingsXpath = dictHelper.joinChildToXpath(parentXpath, self.portIdentifierXpath)
        interfacePropertyXpath = dictHelper.joinChildToXpath(interfaceSettingsXpath, propertyName)

        if (interfacePropertyXpath not in flatternedTemplate):
            raise Exception('Could not find "%s" in interface template' % (interfaceSettingsXpath))
        
        return flatternedTemplate[interfacePropertyXpath]
    
    def getInterfaceZoneName(self, xpath : str, flatternedTemplate : dict) -> str:

        return self.getInterfaceTemplateSettings(xpath, 'zone', flatternedTemplate)
    
    def getInterfaceNetworkIndex(self, xpath : str, flatternedTemplate : dict) -> int:

        return self.getInterfaceTemplateSettings(xpath, 'network-index', flatternedTemplate)

    def getPhysicalPort(self, xpath : str, flatternedTemplate : dict, *args, **kwargs) -> str:

        return self.physicalPort
    
    def getVRF(self, xpath : str, flatternedTemplate : dict, *args, **kwargs) -> str:        

        return self.getInterfaceZoneName(xpath, flatternedTemplate)
    
    def getVlan(self, xpath : str, flatternedTemplate : dict, *args, **kwargs) -> int:        

        zoneName = self.getInterfaceZoneName(xpath, flatternedTemplate)
        networkIndex = self.getInterfaceNetworkIndex(xpath, flatternedTemplate)

        if (zoneName == "DMZ"):
            return 100 + networkIndex
        elif (zoneName == "CORP"):
            return 200 + networkIndex
        else:
            raise Exception("Unknown zone defined in template interface: [%s]" % (zoneName))
        
    def getInterfaceName(self, xpath : str, flatternedTemplate : dict, *args, **kwargs) -> str:        

        zoneName = self.getInterfaceZoneName(xpath, flatternedTemplate)

        return '%s-v%d' % (zoneName, self.getVlan(xpath, flatternedTemplate, *args, **kwargs))


