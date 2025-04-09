from IoManager import *
import Functions.Helper as help


def HighMuxSelect(index : int, yamlData : str = ""):
    """
    Sets the selected output for the high side mux
    """
    if(yamlData == ""):
        #Imports YAML
        yamlData = help.ImportYaml("Io\IoConfig.yaml")
    #Loops through every value in pin dictonary
    for place, pin in yamlData["HighMuxPins"].items():
        #Sets output based on bitmask
        GPIO.output(pin, (index & place != 0))

def LowMuxSelect(index : int, yamlData : str = ""):
    """
    Sets the selected output for the low side mux
    """
    if(yamlData == ""):
        #Imports YAML
        yamlData = help.ImportYaml("Io\IoConfig.yaml")
    #Loops through every value in pin dictonary
    for place, pin in yamlData["LowMuxPins"].items():
        #Sets output based on bitmask
        GPIO.output(pin, (index & place != 0))

def PullHigh(value : bool, yamlData : str = ""):
    """
    Pulls the high side of the mux high. 1 for high, 0 for float
    """
    if(yamlData == ""):
        #Imports YAML
        yamlData = help.ImportYaml("Io\IoConfig.yaml")
    GPIO.output(yamlData["HighEnPin"],value)

def PullLow(value : bool, yamlData : str = ""):
    """
    Pulls the low side of the mux high. 1 for Low, 0 for float
    """
    if(yamlData == ""):
        #Imports YAML
        yamlData = help.ImportYaml("Io\IoConfig.yaml")
    GPIO.output(yamlData["LowEnPin"],value)

def ReadVoltage():
    raise NotImplementedError()

def ReadAmp():
    raise NotImplementedError()

def ReadOhm():
    yamlData = help.ImportYaml("Io\IoConfig.yaml")
    PullHigh(True,yamlData)
    PullLow(True,yamlData)

    vOut = ReadVoltage()
    r1 = 50
    vIn= 3.3
    r2 = (vOut * r1) / (vIn - vOut)

    PullHigh(False,yamlData)
    PullLow(False,yamlData)

    return r2

def ReadContinuity():
    yamlData = help.ImportYaml("Io\IoConfig.yaml")
    PullHigh(True,yamlData)
    PullLow(True,yamlData)
    #Read value here
    isConn = False

    PullHigh(False,yamlData)
    PullLow(False,yamlData)
    return isConn
