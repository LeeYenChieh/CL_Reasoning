from Model.Model import Model
from Dataset.Dataset import Dataset

from Log.Log import Log
from Log.OneDatasetLog import OneDatasetLog
from Log.TwoAgentLog import TwoAgentLog

from Strategy.Strategy import Strategy
from Strategy.onlyChinese import OnlyChinese
from Strategy.onlyEnglish import OnlyEnglish
from Strategy.onlySpanish import OnlySpanish
from Strategy.multiAgent import MultiAgent
from Strategy.chooseAnswer import ChooseAnswer
from Strategy.getOneOutput import GetOneOutput

from Strategy.StrategyType import StrategyType

class RunContext():
    def __init__(self):
        self.strategy: Strategy = None
        self.log: Log = Log()
    
    def setStrategy(self, mode: str):
        if mode == StrategyType.ONLYCHINESE:
            self.strategy = OnlyChinese()
            self.log = OneDatasetLog()

        elif mode == StrategyType.ONLYENGLISH:
            self.strategy = OnlyEnglish()
            self.log = OneDatasetLog()
        
        elif mode == StrategyType.ONLYSPANISH:
            self.strategy = OnlySpanish()
            self.log = OneDatasetLog()

        elif mode == StrategyType.MULTIAGENT:
            self.strategy = MultiAgent()
            self.log = TwoAgentLog()

        elif mode == StrategyType.CHOOSEANSWER:
            self.strategy = ChooseAnswer()
            self.log = TwoAgentLog()
        
        elif mode == StrategyType.GETONEOUTPUT:
            self.strategy = GetOneOutput()
        else:
            print("Strategy doesn't exist.")
            self.strategy = None
    
    def getStrategyName(self) -> str:
        return self.strategy.getName()
    
    def setLog(self, mode: str):
        pass

    def runExperiment(self, model: Model, dataset: Dataset, *args, **kwargs) -> list:
        if(not self.strategy):
            print("You need to set strategy first!")
            return
        return self.strategy.getRes(model, dataset, self.log, *args, **kwargs)
