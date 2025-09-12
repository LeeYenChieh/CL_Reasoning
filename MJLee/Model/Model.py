class Model:
    def __init__(self, tempature: int = 0):
        self.tempature: int = tempature
        self.name: str = ""

    def getName(self) -> str:
        return self.name
    
    def printName(self):
        print(f'Model： {self.name}\n')
        return

    def getRes(self, prompt: str) -> str:
        return ""