from Model.Model import Model
from Model.GPT41mini import GPT41mini
from Model.GPT4omini import GPT4omini
from Model.Deepseek import Deepseek
from Model.Gemini import Gemini
from Model.Gemma import Gemma

class ModelFactory():
    def __init__(self):
        pass

    def buildModel(self, type, *args, **kwargs) -> Model:
        if type == 'gpt4.1mini':
            return GPT41mini(*args, **kwargs)
        elif type == 'gpt4omini':
            return GPT4omini(*args, **kwargs)
        elif type == 'deepseek':
            return Deepseek(*args, **kwargs)
        elif type == 'gemini':
            return Gemini(*args, **kwargs)
        elif type == 'gemma':
            return Gemma(*args, **kwargs)
        else:
            print('Model doesn\'t exist!')
            return None