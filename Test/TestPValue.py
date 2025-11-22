from File.File import File
from Log.Log import Log
from Dataset.DatasetType import get_dataset_map

from Test.Test import Test

class TestPValue(Test):
    def __init__(self):
        super().__init__()
        self.name: str = "Test Exact Match"

    def runTest(self, fileList: list[File], log: Log):
        for file in fileList:
            log.logInfo(file)
            DatasetClass = get_dataset_map()[file.getDatasetName()]
            data = file.getData()
            total = file.getDataNums()
            cnt = 0

            for i in range(total):
                if DatasetClass.compareTwoAnswer(str(data[i]["Answer"]), str(data[i]["MyAnswer"])):
                    cnt += 1
            log.logMessage(f'Performance\n{cnt} / {total}\n{cnt * 100 / total}%')