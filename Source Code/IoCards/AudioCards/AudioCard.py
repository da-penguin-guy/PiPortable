from ..IoCard import *

class AudioCard(IoCard):
    isStereo : bool
    isBal : bool
    isIn : IoTypes
    def __init__(self, slotIndex:int, isI2C:IoTypes = False, I2CAdr:int = None, isUSB: bool = False, usbID:int = None, isStero:bool = False, isBal:bool = False, isIn:bool = False):
        super().__init__(slotIndex, isI2C, I2CAdr, isUSB, usbID)
        self.icon = ConvertIcon("Icons\AudioCardIcon.png")
        self.isStereo = isStero
        self.isBal = isBal
        self.isIn = isIn

    @staticmethod
    def FindFromData(bytes : list[int], cardSlot : int):
        """
        Gets IO Card information from data on EEPROM
        """
        try:
            yamlData = help.getYaml("IoCards/AudioCards/AudioLookup.yaml")
            #try:
            cardInfo = yamlData[bytes[1]]
            #Import Library from path provided
            module = importlib.import_module(help.GetAbsPath(cardInfo["File"]))
            print(module)
            #Get class from string
            cardType = getattr(module, cardInfo["TypeName"])
            return cardType.FindFromData(bytes,cardSlot)
        except:
            raise NotImplementedError("No Audio Card found matches that ID")
