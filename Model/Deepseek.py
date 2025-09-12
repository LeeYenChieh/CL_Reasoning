from Model.Model import Model

class Deepseek(Model):
    def __init__(self, tempature: int = 0):
        super().__init__(tempature)
        self.name: str = "Deepseek"
    
    def getRes(self, prompt) -> str:
        return ""
