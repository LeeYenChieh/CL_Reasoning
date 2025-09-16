from Model.Model import Model
from Dataset.Dataset import Dataset
from Strategy.Strategy import Strategy
from Log.Log import Log

from tqdm import tqdm

class OnlyEnglish(Strategy):
    def __init__(self):
        super().__init__()
        self.name: str = "Only English"

    def translatePrompt(self, question: str) -> str:
        prompt = "Translate the following text into English. If the text is already in English, just output it as-is without any modifications. Translate the entire question including all instructions and JSON format requirements. However, do NOT provide any actual JSON answer - only translate the text. Do not attempt to solve the problem, do not reason or analyze the question, and do not add any comments. Strictly perform language conversion only.\n\n"
        return prompt + question

    def processPrompt(self) -> str:
        prompt = "\nSolve the problem."
        return prompt

    def formatPrompt(self) -> str:
        prompt = f'Please strictly follow the format below for output\n' \
            f'Reasoning process\n' \
            f'{{your reasoning process}}\n\n' \
            f'Your response must end with the exact JSON format specified in the question above.\n'
        return prompt

    def getPrompt(self, question: str) -> str:
        prompt = question + self.processPrompt() + self.formatPrompt()
        return prompt

    def getRes(self, model: Model, dataset: Dataset, log: Log) -> list:
        log.logInfo(self, model, dataset)

        database = dataset.getData()
        answer = dataset.getAnswer()
        result = [{
            "Model": model.getName(),
            "Dataset": dataset.getName(),
            "Strategy": self.name,
            "Data Nums": dataset.getNums(),
            "Data Samples": dataset.getSamples()
        }]

        pbar = tqdm(total=dataset.getDataNum())
        for i in range(dataset.getDataNum()):
            translateQuestion = model.getRes(self.translatePrompt(database[i]))
            resultAnswer = model.getRes(self.getPrompt(translateQuestion))
            result.append({
                "Question": database[i],
                "Translated": translateQuestion,
                "Result": resultAnswer,
                "Answer": answer[i],
                "MyAnswer": self.parseAnswer(resultAnswer)
            })

            log.logMessage(f'翻譯問題：\n{translateQuestion}')
            log.logMessage(f'結果：\n{resultAnswer}')
            log.logMessage(f'My Answer: {result[-1]["MyAnswer"]}\nCorrect Answer: {answer[i]}')
            pbar.update()
        
        pbar.close()

        return result