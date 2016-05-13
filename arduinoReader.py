from serial import Serial
import numpy as np
import binascii
import threading

#autre truc cool : http://stackoverflow.com/questions/676172/full-examples-of-using-pyserial-package
#mais lui il est encore mieux: http://www.jujens.eu/posts/2014/May/05/Communication-serie/


class ArduinoReader:


    def __init__(self):
        self.serial_port = Serial(port='/dev/ttyUSB0', baudrate=230400)
        self.newArduino = False
        self.threadsDieNow = False

    def findNb1Faibles(self, x):
        res = 0
        temp = x
        for i in range(0, 8):
            if temp & 1 == 1:
                res = res + 1
                temp = temp >> 1
            else:
                return res
        return res

    def findNb1Forts(self, x):
        res = 0
        temp = x
        for i in range(0, 8):
            if temp & 128 != 0:
                res = res + 1
                temp = temp << 1
            else:
                return res
        return res

    def calcMasque(self):
        res = 0
        for i in range(0, self.offset):
            res = res << 1 | 1
        self.masque = res

    def findBytes(self, x, y):
        res = x & self.masque
        res = res << (8 - self.offset)
        res = res | (y >> self.offset)
        return res

    def concat(self, faible, fort):
        return faible | (fort << 8)


    def continuousStart(self):
        """CALL THIS to start running forever."""
        self.t = threading.Thread(target=self.readUSB)
        self.t.start()

    def getArduino(self):
        return self.arduino

    def readUSB(self, forever=True):

        res = np.arange(0, 64)
        compteur = 0
        begin = True
        prevInInt = 0
        prevByte = 0

        while True:
            if self.threadsDieNow: break


            # reperer le premier caractere de debut et l'offset de decalage pour chaque octet
            while begin:
                if self.serial_port.inWaiting():

                    if prevInInt != 255:
                        inInt = int(binascii.hexlify(self.serial_port.read(1)), 16)
                    else:
                        prevInInt = 0



                    nb1faibles = self.findNb1Faibles(prevInInt)
                    nb1forts = self.findNb1Forts(inInt)


                    self.offset = nb1faibles
                    if self.offset + nb1forts >= 8:

                        begin = False
                        self.calcMasque()


                    prevInInt = inInt


            if self.serial_port.inWaiting():


                inInt = int(binascii.hexlify(self.serial_port.read(1)), 16)

                curByte = self.findBytes(prevInInt, inInt)

                if compteur < 128:
                    if compteur % 2 ==1:
                        res[compteur/2] = self.concat(prevByte, curByte)/40
                    compteur = compteur + 1

                else:

                    compteur = 0

                    self.arduino = res
                    self.newArduino = True
                    begin = True



                prevByte = curByte
                prevInInt = inInt


                if forever == False:
                    break









