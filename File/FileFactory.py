import json
from File.File import File

from Model.ModelType import MODEL_NAME_DICT, MODEL_LIST
from Dataset.DatasetType import DATASET_NAME_DICT, DATASET_LIST
from Strategy.StrategyType import STRATEGY_NAME_DICT, STRATEGY_LIST

class FileFactory():
    def __init__(self):
        pass
    
    def getFileByPath(self, path: str="") -> File:
        try:
            with open(path, 'r') as f:
                data = json.load(f)
            result = File(datasetName=data[0]["Dataset"], modelName=data[0]["Model"], strategyName=data[0]["Strategy"], nums=data[0]["Data Nums"], sample=data[0]["Data Samples"], data=data[1:])
        except:
            print(f'開啟檔案失敗')
            print(path)
            return None
        return result
    
    def getFileBySetting(self, dir: str="", model: list=None, dataset: list=None, strategy: list=None) -> list:
        if model == None:
            model = MODEL_LIST
        if dataset == None:
            dataset = DATASET_LIST
        if strategy == None:
            strategy = STRATEGY_LIST
        
        result = []
        for m in model:
            for d in dataset:
                for s in strategy:
                    path = f'{dir}/{MODEL_NAME_DICT[m]}_{DATASET_NAME_DICT[d]}_{STRATEGY_NAME_DICT[s]}.json'
                    newFile = self.getFileByPath(path)
                    if newFile:
                        result.append(newFile)
        return result