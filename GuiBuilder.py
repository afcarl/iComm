import os
import sys

os.chdir('Guis')
walkObj = os.walk('.')

prefix = 'pyuic4'
for dirPath, dirNams, fileNames in walkObj:
    os.chdir(dirPath)
    uiFiles = filter(lambda x: '.ui' in x, fileNames)
    for uiFile in uiFiles:
        pyFile = uiFile.split('.')[0] + '.py'
        command = '%s %s -o %s' % (prefix, uiFile, pyFile)
        print command
        os.popen(command)
print 'Completed converting .ui files to .py files'
