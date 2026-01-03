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
    """
    A strategy implementation that translates questions into a specific target language
    before performing reasoning (Chain-of-Thought) to generate an answer.
    """
    def __init__(self, model: Model, dataset: Dataset, log: Log, type):
        super().__init__()
        self.name: str = STRATEGY_TO_NAME[type]
        self.model: Model = model
        self.dataset: Dataset = dataset
        self.log: Log = log
        self.type = type

    def getPrompt(self, question: str) -> str:
        prompt = PromptCOTFactory().getPrompt(self.type, question) + PromptFormatFactory().getPrompt(self.type)
        return prompt

    def getRes(self) -> list:
        self.log.logInfo(self, self.model, self.dataset)

        database = self.dataset.getData()
        result = [{
            "Model": self.model.getName(),
            "Dataset": self.dataset.getName(),
            "Strategy": self.name,
            "Data Nums": self.dataset.getNums(),
            "Data Samples": self.dataset.getSample()
        }]

        pbar = tqdm(total=self.dataset.getDataNums())
        for data in database:
            translateQuestion = self.model.getRes(PromptTranslateFactory().getPrompt(self.type, data["question"]))
            resultAnswer = self.model.getRes(self.getPrompt(translateQuestion))
            result.append({
                "id": data["id"],
                "Question": data["question"],
                "Translated": translateQuestion,
                "Result": resultAnswer,
                "Answer": data["answer"],
                "MyAnswer": self.parseAnswer(resultAnswer)
            })

            self.log.logMessage(f'翻譯問題：\n{translateQuestion}')
            self.log.logMessage(f'結果：\n{resultAnswer}')
            self.log.logMessage(f'My Answer: {result[-1]["MyAnswer"]}\nCorrect Answer: {data["answer"]}')

            pbar.update()
        
        pbar.close()

        return result
    
    @staticmethod
    def getTokenLens(model: Model, data):
        return model.getTokenLens(data["Result"]) + model.getTokenLens(data["Translated"])