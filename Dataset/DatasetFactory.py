from Dataset.Dataset import Dataset
from Dataset.MathQA import MathQA

class DatasetFactory():
    def __init__(self):
        pass

    def buildDataset(self, type, *args, **kwargs) -> Dataset:
        if type == 'mathqa':
            return MathQA(*args, **kwargs)
        else:
            return None
