from File.File import File
from Log.Log import Log
from Dataset.DatasetType import get_dataset_map

from Test.Test import Test
import json

# class TestCaseBase(Test):
#     def __init__(self):
#         super().__init__()
#         self.name: str = "Test Exact Match"

#     def runTest(self, fileList: list[File], log: Log):
#         for file in fileList:
#             print("Use default file(onlyChinese and onlyEnglish output file)!")
#             from Strategy.onlyChinese import OnlyChinese
#             from Strategy.onlyEnglish import OnlyEnglish
#             dataPath1 = f'result/{file.getModelName()}_{file.getDatasetName()}_{OnlyChinese.NAME}.json'
#             dataPath2 = f'result/{file.getModelName()}_{file.getDatasetName()}_{OnlyEnglish.NAME}.json'

#             try:
#                 with open(dataPath1, 'r') as f:
#                     data_cn = json.load(f)
#                 with open(dataPath2, 'r') as f:
#                     data_en = json.load(f)
#             except:
#                 log.logMessage(f'\nRead File Error!')
#                 return []
    
#             log.logInfo(file)
#             DatasetClass = get_dataset_map()[file.getDatasetName()]
#             data = file.getData()
#             total = file.getDataNums()
#             cn_en, cn, en, no = 0, 0, 0, 0
#             cn_co, en_co = 0, 0

#             for i in range(total):
#                 temp_cn_co = DatasetClass.compareTwoAnswer(str(data_cn[i + 1]["Answer"]), str(data_cn[i + 1]["MyAnswer"]))
#                 temp_en_co = DatasetClass.compareTwoAnswer(str(data_en[i + 1]["Answer"]), str(data_en[i + 1]["MyAnswer"]))
#                 temp_final_co = DatasetClass.compareTwoAnswer(str(data[i]["Answer"]), str(data[i]["MyAnswer"]))
#                 if temp_cn_co and temp_en_co:
#                     cn_en += 1
#                 elif temp_cn_co and not temp_en_co:
#                     cn += 1
#                     if temp_final_co:
#                         cn_co += 1
#                 elif not temp_cn_co and temp_en_co:
#                     en += 1
#                     if temp_final_co:
#                         en_co += 1
#                 else:
#                     no += 1

#             log.logMessage(f'Chinese and English: {cn_en}\nChinese: {cn}\nEnglish: {en}\nNo: {no}\nChinese After Framework: {cn_co}\nEnglish After Framework: {en_co}')

from File.File import File
from Log.Log import Log
from Dataset.DatasetType import get_dataset_map

from Test.Test import Test
import json

class TestCaseBase(Test):
    def __init__(self):
        super().__init__()
        self.name: str = "Test Exact Match"
    
    def runTest(self, fileList: list[File], log: Log):
        pass