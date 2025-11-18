from Log.Log import Log
from Log.FileLog import FileLog
from Test.Test import Test

class TestContext():
    def __init__(self):
        self.test: Test = None
        self.log: Log = FileLog()
    
    def setTest(self, test: Test):
        self.test = test
    
    def getTestName(self) -> str:
        return self.test.getName()

    def runTest(self, fileList: list, *args, **kwargs) -> list:
        if(not self.test):
            print("You need to set test method first!")
            return
        return self.test.runTest(fileList, self.log, *args, **kwargs)
