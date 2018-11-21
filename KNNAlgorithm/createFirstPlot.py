
from numpy import *
import matplotlib
import matplotlib.pyplot as plt
import KNN


fig = plt.figure()
ax = fig.add_subplot(111)
datingDataMat, datingDataLables = KNN.file2matrix('datingTestSet2.txt')
ax.scatter(datingDataMat[:, 0], datingDataMat[:, 1], 15.0*array(datingDataLables), 15.0*array(datingDataLables))
#ax.axis([-2, 25, -0.2, 2.0])
plt.xlabel('Percentage of Time Spend Playing Video Game')
plt.ylabel('Liters of Ice Cream Consumed Per Week')
plt.show()