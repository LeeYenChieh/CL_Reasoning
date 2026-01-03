from Model.Model import Model
from Dataset.Dataset import Dataset
from Strategy.OnlyOneLanguage import OnlyOneLanguage
from Log.Log import Log
from Strategy.PromptAbstractFactory.PromptTranslateFactory import PromptTranslateFactory
from File.File import File

from tqdm import tqdm

class Repair(OnlyOneLanguage):
    """
    A strategy designed to 'repair' incomplete results from a previous run.
    It reads data from a file and selectively re-processes items where 'MyAnswer' is empty.
    Inherits from OnlyOneLanguage to reuse the prompt generation logic.
    """
    def __init__(self, model: Model, dataset: Dataset, log: Log, file: File):
        self.name: str = file.getStrategyName()
        self.model: Model = model
        self.dataset: Dataset = dataset
        self.log: Log = log
        self.file = file
        self.type = file.getStrategyName()


    def getRes(self) -> list:
        self.log.logInfo(self, self.model, self.dataset)
        self.log.logMessage("Repair File, ignore dataset nums!")
        repairData = self.file.getData()

        cnt = 0
        for d in repairData:
            if d["MyAnswer"] == "":
                cnt += 1
        self.log.logMessage(f'Repair Data: {cnt} / {self.file.getDataNums()}')

        result = [{
            "Model": self.model.getName(),
            "Dataset": self.dataset.getName(),
            "Strategy": self.name,
            "Data Nums": self.dataset.getNums(),
            "Data Samples": self.dataset.getSample()
        }]

        for fileData in repairData:
            datasetData = self.dataset.getDataById(fileData["id"])
            if datasetData == None:
                raise Exception(f'[Warning] ID mismatch found at id {fileData["id"]}!')

        pbar = tqdm(total=cnt)
        for fileData in repairData:
            if fileData["MyAnswer"] != "":
                result.append(fileData)
                continue
            datasetData = self.dataset.getDataById(fileData["id"])
            translateQuestion = self.model.getRes(PromptTranslateFactory().getPrompt(self.type, datasetData["question"]))
            resultAnswer = self.model.getRes(self.getPrompt(translateQuestion))
            result.append({
                "id": datasetData["id"],
                "Question": datasetData["question"],
                "Translated": translateQuestion,
                "Result": resultAnswer,
                "Answer": datasetData["answer"],
                "MyAnswer": self.parseAnswer(resultAnswer)
            })

            self.log.logMessage(f'翻譯問題：\n{translateQuestion}')
            self.log.logMessage(f'結果：\n{resultAnswer}')
            self.log.logMessage(f'My Answer: {result[-1]["MyAnswer"]}\nCorrect Answer: {datasetData["answer"]}')

            pbar.update()
        pbar.close()

        return result