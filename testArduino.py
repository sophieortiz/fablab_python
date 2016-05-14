from sklearn import svm
import shelve
import numpy as np


if __name__ == "__main__":
    clf = svm.SVC(kernel='rbf')

    r1 = [[100, 70, 50],[100, 90, 80],[100, 50, 30],[100, 40, 35]]
    r2 = [1, 1, 2, 2]

    clf.fit(r1, r2)

    res = clf.predict([90, 50, 30])
    print('res: '+str(res))


