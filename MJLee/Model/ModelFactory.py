from Model.Model import Model
from Model.GPT41mini import GPT41mini

class ModelFactory():
    def __init__(self):
        pass

    def buildModel(self, type, *args, **kwargs) -> Model:
        if type == 'gpt4.1mini':
            return GPT41mini(*args, **kwargs)
        else:
            return None