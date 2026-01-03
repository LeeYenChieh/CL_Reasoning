from File.File import File
from Log.Log import Log
from Test.Test import Test

class PrintOne(Test):
    def __init__(self):
        super().__init__()
        self.name: str = "Print One Sample"

    def runTest(self, fileList: list[File], log: Log):
        if len(fileList) != 1:
            print("You should provide only one file!")
            return
        file: File = fileList[0]
        log.logInfo(file)
        data = file.getData()
        total = file.getDataNums()

        printList = []
        for i in range(total):
            if data[i]["Times"] != 0 and data[i]["Times"] != 3:
                printList.append(i)
        log.logMessage(f'There are {len(printList)} samples.')
        
        while(True):
            index = int(input('Which sample you want to check?\n'))
            d = data[printList[index]]
            log.logMessage(f'Record1: \n{d["Record1"]}')
            log.logMessage(f'Record2: \n{d["Record2"]}')
            log.logMessage(f'Times: \n{d["Times"]}')
            log.logMessage(f'Correct Answer: \n{d["Answer"]}')
            log.logMessage(f'My Answer: \n{d["MyAnswer"]}')