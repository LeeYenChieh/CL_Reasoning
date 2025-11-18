class Model():
    def __init__(self, tempature):
        self.tempature: int = 0 if tempature == None else tempature
        self.name: str = ""

    def getName(self) -> str:
        return self.name
    
    def printName(self):
        print(f'Model： {self.name}')
        return

    def getRes(self, prompt: str) -> str:
        return ""
    
    def getListRes(self, promptList: list) -> list:
        return []