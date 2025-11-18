from Model.Model import Model
from Dataset.Dataset import Dataset
from Strategy.Strategy import Strategy
from Strategy.StrategyType import STRATEGY_TO_NAME
from Log.Log import Log
from Strategy.PromptAbstractFactory.PromptCOTFactory import PromptCOTFactory
from Strategy.PromptAbstractFactory.PromptTranslateFactory import PromptTranslateFactory
from Strategy.PromptAbstractFactory.PromptFormatFactory import PromptFormatFactory


from tqdm import tqdm

class OnlyOneLanguage(Strategy):
    def __init__(self, model: Model, dataset: Dataset, log: Log, type):
        super().__init__()
        self.name: str = STRATEGY_TO_NAME[type]
        self.model = model
        self.dataset = dataset
        self.log = log
        self.type = type

    def getPrompt(self, question: str) -> str:
        prompt = PromptCOTFactory().getPrompt(self.type, question) + PromptFormatFactory().getPrompt(type)
        return prompt

    def getRes(self) -> list:
        self.log.logInfo(self, self.model, self.dataset)

        database = self.dataset.getData()
        answer = self.dataset.getAnswer()
        result = [{
            "Model": self.model.getName(),
            "Dataset": self.dataset.getName(),
            "Strategy": self.name,
            "Data Nums": self.dataset.getNums(),
            "Data Samples": self.dataset.getSamples()
        }]

        pbar = tqdm(total=self.dataset.getDataNum())
        for i in range(self.dataset.getDataNum()):
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