from sklearn import svm
import shelve
import numpy as np



class MachineLearning:



    def guessing(self, data):
        return self.clf.predict(data.reshape(1, -1))

    def guessingInit(self):

        ###init the algorithm
        self.clf = svm.SVC(kernel='rbf')

        ###download the samples and give them to the algorithm
        ls = shelve.open('learned_samples.db', writeback=True)

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


        self.microInput = microInput
        ls = shelve.open('learned_samples.db', writeback=True)
        if not ls.has_key('META'):
            ls['META'] = [0, 0]
            self.microSampleIndex = 0
            self.arduinoSampleIndex = 0

        else:
            self.microSampleIndex = ls['META'][0]
            self.arduinoSampleIndex = ls['META'][1]

        ls.close()

            

    def learn(self, data, result):

        resultArray = np.arange(1)
        resultArray[0] = result


        ls = shelve.open('learned_samples.db', writeback=True)
        if self.microInput:

            ls["micro"+str(self.microSampleIndex)] = [data, resultArray]
            ls['META'][0] = self.microSampleIndex + 1

        else:
            ls["arduino"+str(self.arduinoSampleIndex)] = [data, resultArray]
            ls['META'][1] = self.arduinoSampleIndex + 1
        ls.close()


 
    
