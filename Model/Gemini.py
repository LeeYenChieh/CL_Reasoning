from Model.Model import Model

class Gemini(Model):
    def __init__(self, tempature: int = 0):
        super().__init__(tempature)
        self.name: str = "Gemini"
    
    def getRes(self, prompt) -> str:
        return ""
