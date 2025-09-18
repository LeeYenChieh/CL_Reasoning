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
    
    DATASET_LIST = [MATHQA, COMMENSEQA, MGSM, MMLU, TRUTHFULQA, XCOPA]
    DATASET_MAP = {
        _MathQA.NAME: _MathQA,
        _CommenseQA.NAME: _CommenseQA,
        _MGSM.NAME: _MGSM,
        _MMLU.NAME: _MMLU,
        _TruthfulQA.NAME: _TruthfulQA,
        _XCOPA.NAME: _XCOPA
    }
    DATASET_NAME_DICT = {
        MATHQA: _MathQA.NAME,
        COMMENSEQA: _CommenseQA.NAME,
        MGSM: _MGSM.NAME,
        MMLU: _MMLU.NAME,
        TRUTHFULQA: _TruthfulQA.NAME,
        XCOPA: _XCOPA.NAME
    }

