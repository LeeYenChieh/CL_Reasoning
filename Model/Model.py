class Model():
    def __init__(self, tempature):
        self.name: str = "Model"
        
        if tempature is None:
            print(f"[{self.name}] Notice: 'tempature' is None. Defaulting to 0.")
            self.tempature = 0
        else:
            self.tempature = tempature
            print(f"[{self.name}] Log: 'tempature' set to {self.tempature}.")

    def getName(self) -> str:
        return self.name
    
    def printName(self):
        print(f'Model： {self.name}')
        return
    
    def printTempature(self):
        print(f'Tempature： {self.tempature}')
        return

    def getRes(self, prompt: str) -> str:
        return ""
    
    def getListRes(self, promptList: list) -> list:
        return []
    
    def getTokenLens(self, text) -> int:
        return 0