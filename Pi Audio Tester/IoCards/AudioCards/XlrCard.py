from ..AudioCards.AudioCard import *

class XlrCard(AudioCard):
    def __init__(self, slotIndex : int, isIn : IoTypes = True, I2CAdr : int = None, usbID : int = None):
        super().__init__(slotIndex, True, I2CAdr, True, usbID, False, True, isIn)

    @staticmethod
    def FindFromData(bytes : list[int], cardSlot : int):
        """
        Gets IO Card information from data on EEPROM
        """
        newCard = XlrCard(cardSlot)
        #Byte 2 is i2cAdr
        newCard.I2CAdr = bytes[2]
        #Byte 3 is input/output config
        newCard.isI2C = 0b00000001 & bytes[3]

        newCard.isIn = IoTypes(0b00000110 & bytes[3] >> 1)

        return newCard