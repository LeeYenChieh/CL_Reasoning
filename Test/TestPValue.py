from File.File import File
from Log.Log import Log
from Dataset.DatasetType import get_dataset_map
from scipy import stats

from Test.Test import Test

class TestPValue(Test):
    def __init__(self):
        super().__init__()
        self.name: str = "Test p Value"

    def runTest(self, fileList: list[File], log: Log):
        log.logInfo(fileList[0])
        log.logInfo(fileList[1])
        data1 = fileList[0].getData()
        data2 = fileList[1].getData()
        score1, score2 = [], []
        DatasetClass = get_dataset_map()[fileList[0].getDatasetName()]

        for i in range(fileList[0].getDataNums()):
            if DatasetClass.compareTwoAnswer(str(data1[i]["Answer"]), str(data1[i]["MyAnswer"])):
                score1.append(1)
            else:
                score1.append(0)
            if DatasetClass.compareTwoAnswer(str(data2[i]["Answer"]), str(data2[i]["MyAnswer"])):
                score2.append(1)
            else:
                score2.append(0)
        
        t_stat, p_value = stats.ttest_rel(score1, score2)
        log.logMessage(f'p value: {p_value}\nt stat: {t_stat}')