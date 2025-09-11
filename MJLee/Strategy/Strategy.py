from Model.Model import Model
from Dataset.Dataset import Dataset

import re

class Strategy:
    def __init__(self):
        self.name: str = ""

    def parseAnswer(self, answer: str) -> str:
        result: str = ""
        match = re.search(r"([A-Za-z])\s*$", answer)
        if match:
            result = match.group(1)
        return result

    def getRes(self, model: Model, dataset: Dataset, nums: int) -> list:
        return []