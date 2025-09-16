from Strategy.Strategy import Strategy

class MultiAgent(Strategy):
    def __init__(self):
        super().__init__()
        self.name: str = "Multi Agent"
    
    def getRes(self, model, dataset, log, dataPath1=None, dataPath2=None):
        if dataPath1 == None or dataPath2 == None:
            print("Use default file(onlyChinese and onlyEnglish output file)!")
            from Strategy.onlyChinese import OnlyChinese
            from Strategy.onlyEnglish import OnlyEnglish


        return super().getRes(model, dataset, log)