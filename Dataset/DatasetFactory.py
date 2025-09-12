from Dataset.Dataset import Dataset
from Dataset.MathQA import MathQA
from Dataset.CommenseQA import CommenseQA
from Dataset.MGSM import MGSM
from Dataset.MMLU import MMLU
from Dataset.TruthfulQA import TruthfulQA
from Dataset.XCOPA import XCOPA

class DatasetFactory():
    def __init__(self):
        pass

    def buildDataset(self, type, *args, **kwargs) -> Dataset:
        if type == 'mathqa':
            return MathQA(*args, **kwargs)
        elif type == 'commenseqa':
            return CommenseQA(*args, **kwargs)
        elif type == 'mgsm':
            return MGSM(*args, **kwargs)
        elif type == 'mmlu':
            return MMLU(*args, **kwargs)
        elif type == 'truthfulqa':
            return TruthfulQA(*args, **kwargs)
        elif type == 'xcopa':
            return XCOPA(*args, **kwargs)
        else:
            print('Dataset doesn\'t exist!')
            return None
