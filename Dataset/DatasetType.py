from enum import Enum
from Dataset.MathQA import MathQA as _MathQA
from Dataset.CommenseQA import CommenseQA as _CommenseQA
from Dataset.MGSM import MGSM as _MGSM
from Dataset.MMLU import MMLU as _MMLU
from Dataset.TruthfulQA import TruthfulQA as _TruthfulQA
from Dataset.XCOPA import XCOPA as _XCOPA

class DatasetType(str, Enum):
    MATHQA = "mathqa"
    COMMENSEQA = "commenseqa"
    MGSM = "mgsm"
    MMLU = "mmlu"
    TRUTHFULQA = "truthfulqa"
    XCOPA = "xcopa"

# 直接用 value 取字串列表
DATASET_LIST = [d.value for d in DatasetType]

# key 改成字串，對應 dataset class
DATASET_MAP = {
    "MathQA": _MathQA,
    "CommenseQA": _CommenseQA,
    "MGSM": _MGSM,
    "MMLU": _MMLU,
    "TruthfulQA": _TruthfulQA,
    "XCOPA": _XCOPA
}

# key 改成字串，對應 dataset 名稱
DATASET_NAME_DICT = {
    DatasetType.MATHQA.value: "MathQA",
    DatasetType.COMMENSEQA.value: "CommenseQA",
    DatasetType.MGSM.value: "MGSM",
    DatasetType.MMLU.value: "MMLU",
    DatasetType.TRUTHFULQA.value: "TruthfulQA",
    DatasetType.XCOPA.value: "XCOPA"
}