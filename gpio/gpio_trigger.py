"""
Script reads one of pin states, and if high state is long enough, another scripts is launched
"""

from gpioMaster import GPIO_Master

buttonTime = 2 #jak dlugo ma byc wcisniety przycisk
waitTime = None #jak dlugo czeka na wcisniecie przycisku
inputPin = 11 #pin do ktorego jest podpiety przycisk

def test():
    gpio = GPIO_Master()
    gpio.setPinAsInput(inputPin)
    while True:
        print(gpio.readPinState(inputPin))

def executeScript():
    gpio = GPIO_Master()
    gpio.setPinAsInput(inputPin)
    if (gpio.waitUntilPressed(inputPin, pressedFor=buttonTime, waitFor=waitTime)):
        print("Pressed")
        #TODO script goes here
        return


if __name__ == "__main__":
    executeScript()