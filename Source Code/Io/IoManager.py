import smbus
import RPi.GPIO as GPIO
import spidev
import IoCards.IoCard as Card
import Functions.Helper as help

IoSlotList = [None,None,None,None]

def InitGPIO():
    yamlData = help.ImportYaml("IoConfig.yaml")
    GPIO.setmode(GPIO.BCM)
    for pin in yamlData["SelectPins"].values():
        GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    for pin in yamlData["DetectPins"].values():
        GPIO.setup(pin, GPIO.OUT, pull_up_down=GPIO.PUD_DOWN)

    
def IsCardIn(slot) -> bool:
    if slot > 3 or slot < 0:
        raise IndexError(f"{slot} is out of range")
    
    yamlConfig = help.ImportYaml("Io\IoConfig.yaml")
    #Looks to see if pin is pulled high
    return GPIO.input(yamlConfig["DetectPins"][slot])

def GetCurrentIO(cardIndex: int) -> Card.IoCard:
    #Checks if there is a card in that slot
    if not IsCardIn(cardIndex):
        return None
    #Checks in memory if there is already a card there
    #NOTE: find way to double check info is not outdated
    if not IoSlotList[cardIndex] == None:
        return IoSlotList[cardIndex]
    yamlConfig = help.ImportYaml("Io\IoConfig.yaml")
    #Looks up ID pin
    csPin = yamlConfig["SelectPins"][cardIndex]
    #Config SPI
    spi = spidev.SpiDev()
    spi.open(0, csPin)  # Open SPI bus 0, chip select 0
    spi.max_speed_hz = 1,000,000
    #Send Read command
    spi.xfer2(0x03)
    #Send starting address
    spi.xfer2(0x00)
    #Read response
    response = spi.readbytes(8)
    #End
    spi.close()
    response = [0,0,0,0b01000110]
    print(response)
    #Do the magic of binary and if statements
    newCard = Card.IoCard.FindFromData(cardIndex,response)
    #Set array to found card
    IoSlotList[cardIndex] = newCard
    return newCard