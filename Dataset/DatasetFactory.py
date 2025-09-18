from Dataset.Dataset import Dataset
from Dataset.MathQA import MathQA
from Dataset.CommenseQA import CommenseQA
from Dataset.MGSM import MGSM
from Dataset.MMLU import MMLU
from Dataset.TruthfulQA import TruthfulQA
from Dataset.XCOPA import XCOPA

from Dataset.DatasetType import DatasetType

class DatasetFactory():
    def __init__(self):
        pass

    def buildDataset(self, type, *args, **kwargs) -> Dataset:
        if type == DatasetType.MATHQA.value:
            return MathQA(*args, **kwargs)
        elif type == DatasetType.COMMENSEQA.value:
            return CommenseQA(*args, **kwargs)
        elif type == DatasetType.MGSM.value:
            return MGSM(*args, **kwargs)
        elif type == DatasetType.MMLU.value:
            return MMLU(*args, **kwargs)
        elif type == DatasetType.TRUTHFULQA.value:
            return TruthfulQA(*args, **kwargs)
        elif type == DatasetType.XCOPA.value:
            return XCOPA(*args, **kwargs)
        else:
            print('Dataset doesn\'t exist!')
            return None
