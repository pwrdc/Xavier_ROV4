import Jetson.GPIO as GPIO  # needed package


class GPIO_Master():

  def __init__(self, mode=GPIO.BOARD, debug=True, clean=True):
    if clean:
      GPIO.cleanup()
    self.mode = mode
    self.debug = debug
    GPIO.setmode(self.mode)
    self.inputPins = []
    self.outputPins = []

  def setPinAsInput(self, pinNumber):
    if pinNumber not in self.inputPins:
      if pinNumber in self.outputPins:
        if self.debug:
          print("Changing {} pin to input".format(pinNumber))
        self.outputPins.remove(pinNumber)
      GPIO.setup(pinNumber, GPIO.IN)
      if self.debug:
        print("Pin {} set as input.".format(pinNumber))
      self.inputPins.append(pinNumber)
    else:
      if self.debug:
        print("Pin {} already set as input".format(pinNumber))

  def setPinAsOutput(self, pinNumber, initState=GPIO.LOW):
    if pinNumber not in self.outputPins:
      if pinNumber in self.inputPins:
        if self.debug:
          print("Changing {} pin to output".format(pinNumber))
        self.inputPins.remove(pinNumber)
      GPIO.setup(pinNumber, GPIO.OUT, initial=initState)
      if self.debug:
        print("Pin {} set as output.".format(pinNumber))
        self.outputPins.append(pinNumber)
      else:
        if self.debug:
          print("Pin {} already set as output".format(pinNumber))

  def readPinState(self, pinNumber):
    if GPIO.gpio_function(pinNumber) == GPIO.IN:
      state = GPIO.input(pinNumber)
      if self.debug:
        print("Pin {} state = {}".format(pinNumber, state))
      return state
    else:
      if self.debug:
        print("Pin {} is set as output".format(pinNumber))
      return None

  def setPinState(self, pinNumber, state):
    if GPIO.gpio_function(pinNumber) == GPIO.OUT:
      GPIO.output(pinNumber, state)
      if self.debug:
        print("Pin {} state set as {}".format(pinNumber, state))
    else:
      if self.debug:
        print("Pin {} is set as input".format(pinNumber))

  def setPinHigh(self, pinNumber):
    self.setPinState(pinNumber, GPIO.HIGH)

  def setPinLow(self, pinNumber):
    self.setPinState(pinNumber, GPIO.LOW)

  def waitUntilPressed(self, pinNumber, pressedFor=0.1, waitFor=None):
    """
    waits "waitFor" [s] until pinNumber is pressed for "pressedFor" [ms]
    it waitFor is None, function waits forever
    returns True if pin is pressed
    returns False if tiomeout is reached
    returns None if pin is set as output
    """
    if GPIO.gpio_function(pinNumber) != GPIO.IN:
      if self.debug:
        print("Trying to read from output pin {}.\
               Aborolting, NoneType returned.".format(pinNumber))
        return None

    if waitFor is None:
      GPIO.wait_for_edge(pinNumber, GPIO.RISING)
    else:
      timeout = 1000*waitFor  # convert s to ms
      if (GPIO.wait_for_edge(pinNumber, GPIO.RISING, timeout=int(timeout))) is None:
        if self.debug:
          print("Timeout {} [s] reached, exiting...".format(waitFor))
        return False
    if self.debug:
      print("Got rising signal on pin {}!".format(pinNumber))
    timeout=pressedFor*1000
    if GPIO.wait_for_edge(pinNumber, GPIO.FALLING, timeout=int(timeout)) is not None:
      return False

    else:
     return True
