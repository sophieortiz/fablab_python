from sklearn import svm
import shelve
import numpy as np



class MachineLearning:


    def format(self, datas):
        res = np.arange(0, len(datas)*datas[0].shape[0])
        for i in range(0, len(datas)):
            for j in range(0, datas[0].shape[0]):
                res[i*datas[0].shape[0] + j] = datas[i][j]
        return res

    def guessing(self, data):
        return self.clf.predict(self.format(data).reshape(1, -1))

    def guessingInit(self):

        ###init the algorithm
        self.clf = svm.SVC(kernel='poly')

        ###download the samples and give them to the algorithm
        ls = shelve.open(self.biblio, writeback=True)

        samplesList = []
        if self.microInput:

            resultsArray = np.arange(0, self.microSampleIndex)

            for i in range(0, self.microSampleIndex):
                samplesList.append(ls["micro" + str(i)][0])
                resultsArray[i] = ls["micro" + str(i)][1]

        else:
            resultsArray = np.arange(0, self.arduinoSampleIndex)

            for i in range(0, self.arduinoSampleIndex):
                samplesList.append(ls["arduino" + str(i)][0])
                resultsArray[i] = ls["arduino" + str(i)][1]

        samplesArray = np.array(samplesList)

        self.clf.fit(samplesArray, resultsArray)
        ls.close()

    def __init__(self, microInput):

        self.biblio = 'learned_samples5.db'


        self.microInput = microInput
        ls = shelve.open(self.biblio, writeback=True)
        if not ls.has_key('META'):
            ls['META'] = [0, 0]
            self.microSampleIndex = 0
            self.arduinoSampleIndex = 0

        else:
            self.microSampleIndex = ls['META'][0]
            self.arduinoSampleIndex = ls['META'][1]

        ls.close()

        print('DEBUG: nb samples arduino: ' + str(self.arduinoSampleIndex))

            

    def learn(self, data, result):

        resultArray = np.arange(1)
        resultArray[0] = result


        ls = shelve.open(self.biblio, writeback=True)
        if self.microInput:

            ls["micro"+str(self.microSampleIndex)] = [self.format(data), resultArray]
            ls['META'][0] = self.microSampleIndex + 1

        else:
            ls["arduino"+str(self.arduinoSampleIndex)] = [self.format(data), resultArray]
            ls['META'][1] = self.arduinoSampleIndex + 1
        ls.close()


 
    
