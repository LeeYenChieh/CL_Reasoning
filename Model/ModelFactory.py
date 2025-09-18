from Model.Model import Model
from Model.GPT41mini import GPT41mini
from Model.GPT4omini import GPT4omini
from Model.Deepseek import Deepseek
from Model.Gemini import Gemini
from Model.Gemma import Gemma

from Model.ModelType import ModelType

class ModelFactory():
    def __init__(self):
        pass

    def buildModel(self, type, *args, **kwargs) -> Model:
        if type == ModelType.GPT41MINI.value:
            return GPT41mini(*args, **kwargs)
        elif type == ModelType.GPT4OMINI.value:
            return GPT4omini(*args, **kwargs)
        elif type == ModelType.DEEPSEEK.value:
            return Deepseek(*args, **kwargs)
        elif type == ModelType.GEMINI.value:
            return Gemini(*args, **kwargs)
        elif type == ModelType.GEMMA.value:
            return Gemma(*args, **kwargs)
        else:
            print('Model doesn\'t exist!')
            return None