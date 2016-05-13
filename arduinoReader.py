from serial import Serial

#autre truc cool : http://stackoverflow.com/questions/676172/full-examples-of-using-pyserial-package
#mais lui il est encore mieux: http://www.jujens.eu/posts/2014/May/05/Communication-serie/


class ArduinoReader:

    #hypothese robin envoie les données lignes par lignes a la vitesse 9600 baud/s

    def __init__(self):
        self.serial_port = Serial(port='/dev/ttyUSB0', baudrate=230400)



    def read(self):
        inflow = self.serial_port.readline()
        if inflow[0:8] != "11111111":
            print('Ya pas les 8 1 de debut')
            return
        else:
            res = range(0, 128)
            for i in range(0, 128):
                res[i] = inflow[8+16*i:24+16*i]
            return res

