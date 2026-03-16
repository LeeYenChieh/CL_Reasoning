from File.File import File
from Log.Log import Log
from Model.ModelType import ModelType
from Model.ModelFactory import ModelFactory
from Strategy.StrategyType import get_strategy_map
from Test.Test import Test

class TestTokenNums(Test):
    def __init__(self):
        super().__init__()
        self.name: str = "Test Token Nums"

    def runTest(self, fileList: list[File], log: Log):
        for file in fileList:
            log.logInfo(file)
            
            # 適配最新的 File.py，取得 config
            model_config = file.getModelConfig()
            strategy_config = file.getStrategyConfig()
            strategy_type = strategy_config.strategyType
            strategy_cls = get_strategy_map()[strategy_type]
            
            # 1. 實例化 Model (為了呼叫 model.getTokenLens 取得精準的 tokenizer 計算)
            try:
                model = ModelFactory().buildModel(ModelType(model_config.modelType), model_config)
            except Exception as e:
                log.logMessage(f"❌ 無法建立 Model: {e}")
                continue

            # 2. 從 records_map 取得所有資料
            data = list(file.records_map.values())
            total = len(data)
            
            if total == 0:
                log.logMessage("⚠️ 檔案無資料 (0 records)")
                continue

            cnt = 0

            for record in data:
                cnt += strategy_cls.getTokenLens(model, record)

            log.logMessage(f'Token Nums: {cnt / total}')
            
            file.updateMetadata("Average Token Nums", cnt / total)
            file.save()