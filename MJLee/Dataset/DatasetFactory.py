from Dataset.Dataset import Dataset
from Dataset.MathQA import MathQA

class DatasetFactory():
    def __init__(self):
        pass

    def buildDataset(self, type) -> Dataset:
        if type == 'mathqa':
            return MathQA
        else:
            return None
