from File.File import File
from Log.Log import Log

class Test():
    def __init__(self):
        self.name: str = ""
    
    def printName(self):
        print(f'Test {self.name}')
    
    def getName(self) -> str:
        return self.name

    def runTest(self, fileList: list[File], log: Log):
        return
