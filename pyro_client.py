import Pyro4
'''
Simple Pyro4 client capable of using all methods that
RPi_ROV4 Communication class enables.
'''

if __name__ == '__main__':
    try:
        Pyro4.locateNS()
        rpi_reference = Pyro4.Proxy("PYRONAME:RPI_communication")
    except Exception as err:
        print (err)
