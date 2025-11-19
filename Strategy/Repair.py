from Model.Model import Model
from Dataset.Dataset import Dataset
from Strategy.OnlyOneLanguage import OnlyOneLanguage
from Strategy.StrategyType import STRATEGY_TO_NAME
from Log.Log import Log
from Strategy.PromptAbstractFactory.PromptCOTFactory import PromptCOTFactory
from Strategy.PromptAbstractFactory.PromptTranslateFactory import PromptTranslateFactory
from Strategy.PromptAbstractFactory.PromptFormatFactory import PromptFormatFactory
from File.File import File

from tqdm import tqdm

class Repair(OnlyOneLanguage):
    def __init__(self, model: Model, dataset: Dataset, log: Log, file: File):
        super().__init__()
        self.name: str = file.getStrategyName()
        self.model = model
        self.dataset = dataset
        self.log = log
        self.file = file
        self.type = file.getStrategyName()


    def getRes(self) -> list:
        self.log.logInfo(self, self.model, self.dataset)
        repairData = self.file.getData()

        cnt = 0
        for d in repairData:
            if d["MyAnswer"] == "":
                cnt += 1
        self.log.logMessage(f'Repair Data: {cnt} / {self.file.getDataNums}')

        database = self.dataset.getData()
        answer = self.dataset.getAnswer()
        result = [{
            "Model": self.model.getName(),
            "Dataset": self.dataset.getName(),
            "Strategy": self.name,
            "Data Nums": self.dataset.getNums(),
            "Data Samples": self.dataset.getSample()
        }]

        pbar = tqdm(total=cnt)
        for i in range(self.dataset.getDataNum()):
            if repairData[i]["MyAnswer"] != "":
                result.append(repairData[i])
                continue
            
            translateQuestion = self.model.getRes(PromptTranslateFactory().getPrompt(self.type, database[i]))
            resultAnswer = self.model.getRes(self.getPrompt(translateQuestion))
            result.append({
                "Question": database[i],
                "Translated": translateQuestion,
                "Result": resultAnswer,
                "Answer": answer[i],
                "MyAnswer": self.parseAnswer(resultAnswer)
            })

            self.log.logMessage(f'翻譯問題：\n{translateQuestion}')
            self.log.logMessage(f'結果：\n{resultAnswer}')
            self.log.logMessage(f'My Answer: {result[-1]["MyAnswer"]}\nCorrect Answer: {answer[i]}')

            pbar.update()
        
        pbar.close()

        return result