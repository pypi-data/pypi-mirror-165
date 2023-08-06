
import testModule.JovyTesting.res.jmaths as jmaths

#from testModule.JovyTesting.jmaths import *


class JMATHCLASS():
    """The Mathematics class for JovyTesting"""
    def __init__(self):
        self.add = jmaths.add
        self.sub = self.subtract= jmaths.sub

    def __repr__(self):
        return "The mathematics class for JovyTesting"

    def __str__(self):
        return "The mathematics class for JovyTesting"




jmath = JMATHCLASS()