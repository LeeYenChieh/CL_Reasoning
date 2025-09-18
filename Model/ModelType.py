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
    
    MODEL_LIST = [m for m in (GPT41MINI, GPT4OMINI, DEEPSEEK, GEMINI, GEMMA)]
    MODEL_NAME_DICT = {
        GPT41MINI: _GPT41mini.NAME,
        GPT4OMINI: _GPT4omini.NAME,
        DEEPSEEK: _Deepseek.NAME,
        GEMINI: _Gemini.NAME,
        GEMMA: _Gemma.NAME
    }
