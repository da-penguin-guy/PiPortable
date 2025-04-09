from Functions.Helper import *
import importlib
from enum import Enum

class IoTypes(Enum):
    """
    An Enum to show Input/Output types\n
    0 = Input\n
    1 = Output\n
    2 = Dynamic\n
    3 = None
    """
    I = 0
    O = 1
    Dynamic = 2
    NA = 3

class IoCard:
    """
    A card that goes into any of the 4 IO Slots
    Attributes: 
    """
    slotIndex : int
    isI2C : bool
    I2CAdr : int
    isUSB : bool
    usbID : str
    icon : ctk.CTkImage
    
    def __init__(self, slotIndex:int, isI2C:bool = False, I2CAdr:int = None, isUSB: bool = False, usbID:str = None):
        self.slotIndex = slotIndex
        self.isI2C = isI2C
        self.I2CAdr = I2CAdr
        self.isUSB = isUSB
        self.usbID = usbID
    @staticmethod
    def FindFromData(cardSlot : int, bytes : list[int]):
        """
        Gets IO Card information from data on EEPROM
        """
        yamlData = ImportYaml("IoCards\IoCatagories.yaml")
        #First byte is the Catagory Byte
        #try:
        cardInfo = yamlData["BitLookup"][bytes[0]]
        #Import Library from path provided
        module = importlib.import_module(cardInfo["File"])
        print(module)
        #Get class from string
        cardType = getattr(module, cardInfo["TypeName"])
        return cardType.FindFromData(bytes,cardSlot)
        #except:
            #raise NotImplementedError("No IO Card found matches that ID")