from File.File import File
from Log.Log import Log
from Dataset.DatasetType import DATASET_MAP

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
            if str(data[i]["Prompt"]):
                printList.append(i)
        log.logMessage(f'There are {len(printList)} samples.')
        
        while(True):
            index = int(input('Which sample you want to check?\n'))
            d = data[printList[index]]
            log.logMessage(f'Prompt: \n{d["Prompt"]}')
            log.logMessage(f'Result: \n{d["Result"]}')
            log.logMessage(f'Correct Answer: \n{d["Answer"]}')
            log.logMessage(f'My Answer: \n{d["MyAnswer"]}')