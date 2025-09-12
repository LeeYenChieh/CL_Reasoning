from Model.Model import Model

class Gemma(Model):
    def __init__(self, tempature: int = 0):
        super().__init__(tempature)
        self.name: str = "Gemma"
    
    def getRes(self, prompt) -> str:
        return ""
