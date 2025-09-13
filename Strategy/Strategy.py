from Model.Model import Model
from Dataset.Dataset import Dataset
from Log.Log import Log

import re

class Strategy():
    def __init__(self):
        self.name: str = ""
    
    def printName(self):
        print(f'Strategy {self.name}')

    def parseAnswer(self, answer: str) -> str:
        import json
        result: str = ""
        
        # Try to extract JSON format first: {"answer": "value"}
        json_match = re.search(r'\{"answer":\s*"([^"]+)"\}', answer)
        if json_match:
            result = json_match.group(1).strip().lower()
            return result
        
        # Fallback to original pattern matching
        match = re.search(r"([A-Za-z])\s*$", answer)
        if match:
            result = match.group(1)
        return result
    
    def getName(self) -> str:
        return self.name

    def getRes(self, model: Model, dataset: Dataset, log: Log) -> list:
        return []