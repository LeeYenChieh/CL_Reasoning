from Model.Model import Model
from Dataset.Dataset import Dataset
from Log.Log import Log

import re

class Strategy:
    def __init__(self):
        self.name: str = ""
    
    def printName(self):
        print(f'Strategy {self.name}\n')

    def parseAnswer(self, answer: str) -> str:
        result: str = ""
        match = re.search(r"([a-z])\s*$", answer)
        if match:
            result = match.group(1)
        return result

    def getRes(self, model: Model, dataset: Dataset, log: Log) -> list:
        return []