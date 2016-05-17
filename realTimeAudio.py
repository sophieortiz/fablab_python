import ui_plot
import sys
import numpy as np
from scipy import stats
from PyQt4 import QtCore, QtGui
import PyQt4.Qwt5 as Qwt
from recorder import *
import peak_detect as peak
import os
from math import *
from machineLearning import *
from arduinoReader import *

def plotSomething():

    global microInput
    global curWait
    global learn
    global result
    global ml
    global code
    global absCpt
    global newOpenHabAction
    global it_light
    global it_rollershutter


    if microInput:
        newInput = SR.newAudio
    else:
        newInput = AR.newArduino

    if newInput==False:
        return

    if microInput:
        xs,ys=SR.fft()
    else:
        global xAr
        xs= xAr
        ys = AR.getArduino()


    c.setData(xs,ys)
    uiplot.qwtPlot.replot()
    ### START peak detection ###
    _max, _min = peak.peakdetect(ys, xs, 30, 0.30)

    slope, intercept, r_value, p_value, std_err = stats.linregress(xs,ys)
    THRESHOLD = 10000
    thresholdIsReached = ys > THRESHOLD
    thresholdIsReached[1:][thresholdIsReached[:-1] & thresholdIsReached[1:]] = False
    iterateur = 1
    if thresholdIsReached.any():
		print "Lin Reg: ", slope, "Peaks detected: ",_max
		#print "iterateur: ", iterateur
		#if iterateur%2==0:
		#    os.system('curl --header "Content-Type: text/plain" --request PUT --data "ON" http://localhost:8080/rest/items/Light_Gest/state')
		#else:
		 #   print "off"
		  #  os.system('curl --header "Content-Type: text/plain" --request PUT --data "OFF" http://localhost:8080/rest/items/Light_Gest/state') 
    ### END peak detection ###

	### START signal analysis ###

    curMean = np.mean(ys)
    s = str(curMean)
    global ct
    global datas




    if (curMean > HITLIMIT or curWait > 0) and ct > BEGINCOUNT:

        if curWait < WAITLIMIT:
            datas.append(ys)
            print('on a rentre 1 data. curwait: ' + str(curWait) +' ct: ' + str(absCpt)+  ' curMean ' + str(curMean))
            curWait += 1
        else:
            if learn:

                print('len data: '+str(len(datas)))

                ml.learn(datas, result)

                #voir si on peut pas faire une fermeture du realtimeaudio un peu plus propre
                #sys.exit(0)
            else:
                openHabAction = ml.guessing(datas)
                ct = 0
                print('OPEN HAB ACTION: '+str(openHabAction))
                newOpenHabAction = True
            curWait = 0
            datas = []
    else:
        ct += 1

    absCpt +=1
            
	### END signal analysis ###

    ###Partie Liaison avec OpenHab, c'est pour toi Leslie

    if newOpenHabAction:
        ###Fais ton truc, ici c'est la variable openHabAction qui vaut un npArray de taille 1 avec l'entier
        ###resutat dedans
   
		### 1 Light_Gest
        ### 2 shutter_GF_living
		### 3 temperature up si 1 et down sinon -> traitement openhab
		
		# ou est tabactions ? 
		if openHabAction[0]==1 : 
			#pour l'instant juste pour allumer
			it_light = it_light + 1
			if (it_light%2 == 0) :
				os.system('curl --header "Content-Type: text/plain" --request PUT --data "ON" http://localhost:8080/rest/items/Light_Gest/state')
			else : 
				os.system('curl --header "Content-Type: text/plain" --request PUT --data "OFF" http://localhost:8080/rest/items/Light_Gest/state')
		elif openHabAction[0]== 3 : 
			it_rollershutter = it_rollershutter + 1
			if (it_rollershutter%2 == 0) :
				os.system('curl --header "Content-Type: text/plain" --request PUT --data "ON" http://localhost:8080/rest/items/RollerShutter_Gest/state')
			else : 
				os.system('curl --header "Content-Type: text/plain" --request PUT --data "OFF" http://localhost:8080/rest/items/RollerShutter_Gest/state')    
		elif openHabAction[0]==2 :
			if (it_up%2 == 0) :
				os.system('curl --header "Content-Type: text/plain" --request PUT --data "ON" http://localhost:8080/rest/items/Temp_Gest_Up/state')
			else : 
				os.system('curl --header "Content-Type: text/plain" --request PUT --data "OFF" http://localhost:8080/rest/items/Temp_Gest_Up/state')			
		elif openHabAction[0]==4 : 
			if (it_down%2 == 0) :
				os.system('curl --header "Content-Type: text/plain" --request PUT --data "ON" http://localhost:8080/rest/items/Temp_Gest_Down/state')
			else : 
				os.system('curl --header "Content-Type: text/plain" --request PUT --data "OFF" http://localhost:8080/rest/items/Temp_Gest_Down/state')
		else : 				
			print("Etrange")

		newOpenHabAction = False


    ####Fin de cette partie

    if microInput:
        SR.newAudio=False
    else:
        AR.newArduino = False


    
if __name__ == "__main__":

    microInput = True
    procede = False
    learn = False
    global newOpenHabAction
    newOpenHabAction = False

    global it_rollershutter 
    it_rollershutter = 1
    global it_light 
    it_light = 1


    global absCpt
    absCpt = 0

    global ct
    ct = 0
    global datas
    datas = []

    ###Arguments analysis
    
    if len(sys.argv) == 2 or len(sys.argv) == 4:
            if sys.argv[1] == "micro":
                procede = True
            elif sys.argv[1] == "arduino":
                microInput = False
                procede = True
            else:
                procede = False

            if len(sys.argv) == 4:
                if sys.argv[2] == "learn":
                    procede = True
                    learn = True
                    result = sys.argv[3]
                else:
                    procede = False
    if len(sys.argv) == 1:
        procede = True



    ###Parameters for analysis
    if microInput:
        HITLIMIT = 2000
        WAITLIMIT = 7
        BEGINCOUNT = 10
    else:
        HITLIMIT = 400
        WAITLIMIT = 15

        BEGINCOUNT = 10
        global xAr
        xAr = np.arange(0,64)

    curWait = 0


    if procede:
        ml=MachineLearning(microInput)
        if not learn:
            ml.guessingInit()


        app = QtGui.QApplication(sys.argv)
        win_plot = ui_plot.QtGui.QMainWindow()
        uiplot = ui_plot.Ui_win_plot()
        uiplot.setupUi(win_plot)
        uiplot.btnA.clicked.connect(plotSomething)
        uiplot.btnB.clicked.connect(lambda: uiplot.timer.setInterval(100.0))
        uiplot.btnC.clicked.connect(lambda: uiplot.timer.setInterval(10.0))
        uiplot.btnD.clicked.connect(lambda: uiplot.timer.setInterval(1.0))
        c=Qwt.QwtPlotCurve()
        c.attach(uiplot.qwtPlot)

        if microInput:
            ordo = 1000
        else:
            ordo = 1000

        uiplot.qwtPlot.setAxisScale(uiplot.qwtPlot.yLeft, 0, ordo)
    
        uiplot.timer = QtCore.QTimer()
        uiplot.timer.start(1.0)

    
        win_plot.connect(uiplot.timer, QtCore.SIGNAL('timeout()'), plotSomething) 
    
        if microInput:
            SR=SwhRecorder()
            SR.setup()
            SR.continuousStart()
        else:
            AR = ArduinoReader()
            AR.continuousStart()

        ### DISPLAY WINDOWS
        win_plot.show()
        code=app.exec_()
        if microInput:
            SR.close()
        sys.exit(code)
    else:
        print('Erreur dans les arguments: precisez l\'entree (\"micro\" ou \"arduino\") suivi de learn et de la valeur retour pour apprendre un echantillon.')

    
    
    
    
    
    
    
