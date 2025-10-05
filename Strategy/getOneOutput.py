from Model.Model import Model
from Strategy.Strategy import Strategy
from Log.Log import Log

class GetOneOutput(Strategy):
    NAME = "Get One Output"
    def __init__(self):
        super().__init__()
        self.name: str = GetOneOutput.NAME
    
    def getPrompt(self):
        prompt = input('Input your prompt:\n')
        return prompt
    
    def getRes(self, model: Model, dataset, log: Log) -> list:
        model.printName()
        prompt = self.getPrompt()
        resultOutput = model.getRes(prompt)
        log.logMessage(f'Prompt：{prompt}')
        log.logMessage(f'結果：\n{resultOutput}')

        return