
import os

print(os.getcwd())
#import res.jmaths as jmaths

#from testModule.JovyTesting.jmaths import *

jmaths = {"add":1,"sub":1}
class JMATHCLASS():
    """The Mathematics class for JovyTesting"""
    def __init__(self):
        self.add = 1 #jmaths.add
        self.sub = self.subtract= 1 #jmaths.sub

    def __repr__(self):
        return "The mathematics class for JovyTesting"

    def __str__(self):
        return "The mathematics class for JovyTesting"




jmath = JMATHCLASS()