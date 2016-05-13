from serial import Serial
import serial.tools.list_ports
import numpy as np
import binascii


def findNb1Faibles(x):
    res = 0
    for i in range(0,8):
        if x&1 ==1:
            res = res + 1
            x>>1
        else:
            return res
    return res

def findNb1Forts(x):
    res = 0
    for i in range(0,8):
        if x&64 != 0:
            res = res + 1
            x<<1
        else:
            return res
    return res

def calcMasque(offset):
    res = 0
    for i in range(0,offset):
        res = res<<1|1
    return res

def findBytes(x, y, offset, masque):
    res = x&masque
    res = res<<(8-offset)
    res = res|(y>>offset)
    return res




if __name__ == "__main__":

    serial_port = Serial(port='/dev/ttyUSB0', baudrate=230400)

    print('port ouvert')

    res = np.arange(0,128)
    compteur = 0


    #reperer le premier caractere de debut et l'offset de decalage pour chaque octet
    begin = True
    prevInInt = 0

    while begin:
        if serial_port.inWaiting():
            inInt = int(binascii.hexlify(serial_port.read(1)), 16)
            print('inInt dans begin: '+str(inInt))

            offset = findNb1Faibles(prevInInt)
            if offset +  findNb1Forts(inInt) >= 8:
                print('on a reconnu le caractere de debut')
                begin = False
                masque = calcMasque(offset)

            prevInInt = inInt




    while True:
        if serial_port.inWaiting():

            inInt = int(binascii.hexlify(serial_port.read(1)), 16)

            curByte = findBytes(prevInInt, inInt, offset, masque)

            if compteur < 128:
                res[compteur] = curByte
                compteur = compteur + 1

            else:
                compteur = 0
                if curByte == 255:
                    print('succes')
                else:
                    print('echec')

            prevInInt = inInt

            print('curByte: ' + str(bin(curByte)[2:]) + ' compteur: ' + str(compteur))


