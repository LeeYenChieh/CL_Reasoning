from Model.Model import Model
from Dataset.Dataset import Dataset

from Strategy.Strategy import Strategy
from Strategy.onlyChinese import OnlyChinese
from Strategy.onlyEnglish import OnlyEnglish

class Context:
    def __init__(self):
        self.strategy: Strategy = None
    
    def setStrategy(self, mode: str):
        if mode == "onlyChinese":
            self.strategy = OnlyChinese()
        elif mode == "onlyEnglish":
            self.strategy = OnlyEnglish()
        else:
            print("Strategy doesn't exist.")
            self.strategy = None

    def runExperiment(self, model: Model, dataset: Dataset):
        if(not self.strategy):
            print("You need to set strategy first!")
            return
        self.strategy.getRes(model, dataset)
