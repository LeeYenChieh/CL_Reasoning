from Model.Model import Model
from Strategy.Strategy import Strategy
from Strategy.StrategyType import StrategyNameType
from Log.Log import Log

class GetOneOutput(Strategy):
    NAME = StrategyNameType.GETONEOUTPUT
    def __init__(self, model: Model, dataset, log: Log):
        super().__init__()
        self.name: str = GetOneOutput.NAME
        self.model = model
        self.dataset = dataset
        self.log = log
    
    def getPrompt(self):
        prompt = input('Input your prompt:\n')
        return prompt
    
    def getRes(self) -> list:
        self.model.printName()
        prompt = self.getPrompt()
        resultOutput = self.model.getRes(prompt)
        self.log.logMessage(f'Prompt：{prompt}')
        self.log.logMessage(f'結果：\n{resultOutput}')

        return