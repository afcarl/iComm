from PyQt4.QtGui  import *
from PyQt4.QtCore import *

import pickle

file   = open('saveTest.pkl', 'wb')
pointF = QPointF(0, 0)
print pointF.getAllDataAsPythonList()
pickle.dump(file, pointF)
file.close()
