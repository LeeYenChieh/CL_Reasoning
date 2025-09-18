from enum import Enum

from Model.GPT41mini import GPT41mini as _GPT41mini
from Model.GPT4omini import GPT4omini as _GPT4omini
from Model.Deepseek import Deepseek as _Deepseek
from Model.Gemini import Gemini as _Gemini
from Model.Gemma import Gemma as _Gemma

class ModelType(str, Enum):
    GPT41MINI = 'gpt4.1mini'
    GPT4OMINI = 'gpt4omini'
    DEEPSEEK = 'deepseek'
    GEMINI = 'gemini'
    GEMMA = 'gemma'
    
MODEL_LIST = [m.value for m in ModelType]
MODEL_NAME_DICT = {
    ModelType.GPT41MINI.value: _GPT41mini.NAME,
    ModelType.GPT4OMINI.value: _GPT4omini.NAME,
    ModelType.DEEPSEEK.value: _Deepseek.NAME,
    ModelType.GEMINI.value: _Gemini.NAME,
    ModelType.GEMMA.value: _Gemma.NAME
}
