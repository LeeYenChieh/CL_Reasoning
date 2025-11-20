from Model.Model import Model
from Dataset.Dataset import Dataset
from Strategy.Strategy import Strategy
from Strategy.StrategyType import StrategyNameType
from Log.Log import Log
from File.File import File
from Strategy.PromptAbstractFactory.PromptFormatFactory import PromptFormatFactory
from Strategy.PromptAbstractFactory.PromptSelfReflectionCOTFacroty import PromptSelfReflectionCOTFacroty


from tqdm import tqdm

class SelfReflection(Strategy):
    NAME = StrategyNameType.SELFREFLECTION.value
    def __init__(self, model: Model, dataset: Dataset, log: Log, dataFile: File):
        super().__init__()
        self.name: str = SelfReflection.NAME
        self.model = model
        self.dataset = dataset
        self.log = log
        self.dataFile = dataFile
        self.type = self.dataFile.getStrategyName()

    def getPrompt(self) -> str:
        prompt = PromptSelfReflectionCOTFacroty().getPrompt(self.type) + PromptFormatFactory().getPrompt(self.type)
        return prompt

    def getRes(self) -> list:
        self.log.logInfo(self, self.model, self.dataset)

        if self.dataFile.getDataNums() != self.dataset.getDataNums() or self.dataFile.getModelName() != self.model.getName() \
            or self.dataFile.getDatasetName() != self.dataset.getName():

            self.log.logMessage("Setting doesn't match")
            return []

        database = self.dataset.getData()
        fileData = self.dataFile.getData()
        answer = self.dataset.getAnswer()
        result = [{
            "Model": self.model.getName(),
            "Dataset": self.dataset.getName(),
            "Strategy": self.name,
            "Data Nums": self.dataset.getNums(),
            "Data Samples": self.dataset.getSample()
        }]

        pbar = tqdm(total=self.dataset.getDataNums())
        for i in range(self.dataset.getDataNums()):
            question, output = fileData[i]["Translated"], fileData[i]["Result"]
            record = [
                {"role": "user", "content": question},
                {"role": "assistant", "content": output},
                {"role": "user", "content": self.getPrompt()}
            ]
            resultAnswer = self.model.getListRes(record)
            result.append({
                "Question": database[i],
                "Translated": question,
                "Response": output,
                "Result": resultAnswer,
                "Answer": answer[i],
                "MyAnswer": self.parseAnswer(resultAnswer)
            })

            self.log.logMessage(f'問題：\n{question}')
            self.log.logMessage(f'Response：\n{output}')
            self.log.logMessage(f'結果：\n{resultAnswer}')
            self.log.logMessage(f'My Answer: {result[-1]["MyAnswer"]}\nCorrect Answer: {answer[i]}')

            pbar.update()
        
        pbar.close()

        return result