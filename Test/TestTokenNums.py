from File.File import File
from Log.Log import Log
from Model.ModelType import get_model_map
from Model.Model import Model
from Strategy.StrategyType import get_strategy_map, StrategyNameType
from Strategy.Strategy import Strategy

from Test.Test import Test

class TestTokenNums(Test):
    def __init__(self):
        super().__init__()
        self.name: str = "Test Token Nums"

    def runTest(self, fileList: list[File], log: Log):
        for file in fileList:
            log.logInfo(file)
            strategy = get_strategy_map()[file.getStrategyName()]
            model: Model = get_model_map()[file.getModelName()](0)
            data = file.getData()
            total = file.getDataNums()
            cnt = 0
            cnt_challenge = 0
            total_challenge = 0

            for i in range(total):
                lens = strategy.getTokenLens(model, data[i])
                cnt += lens
                if file.getStrategyName() == StrategyNameType.CHALLENGE.value and data[i]["Times"] != 0:
                    cnt_challenge += lens
                    total_challenge += 1
            
            if file.getStrategyName() == StrategyNameType.CHALLENGE.value:
                log.logMessage(f'Average Token: {cnt / total}\nAverage Token(Only Debate): {cnt_challenge / total_challenge}')
            else:
                log.logMessage(f'Average Token: {cnt / total}')