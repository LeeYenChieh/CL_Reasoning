from Model.Model import Model
from Dataset.Dataset import Dataset
from Strategy.Strategy import Strategy
from Log.Log import Log

from tqdm import tqdm

class OnlyEnglish(Strategy):
    def __init__(self):
        super().__init__()
        self.name: str = "Only English"

    def translatePrompt(question: str) -> str:
        prompt = "Translate the following text into English. Do not attempt to solve the problem, do not reason or analyze the question, and do not add any comments. Strictly perform language conversion only. Do not output any information about the answer or the process, only output the translation of the original question.\n\n"
        return prompt + question

    def processPrompt() -> str:
        prompt = "\nSolve the problem."
        return prompt

    def formatPrompt() -> str:
        prompt = f'Please strictly follow the format below for output\n' \
            f'Reasoning process\n' \
            f'{{your reasoning process}}\n\n' \
            f'Answer\n' \
            f'{{your answer (must be a single English letter)}}\n'
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
            "Strategy": self.name
        }]

        pbar = tqdm(total=dataset.getDataNum())
        for i in range(dataset.getDataNum()):
            translateQuestion = model.getRes(self.translatePrompt(database[i]))
            result = model.getRes(self.getPrompt(translateQuestion))
            result.append({
                "Question": database[i],
                "Translated": translateQuestion,
                "Result": result,
                "Answer": answer[i],
                "MyAnswer": self.parseAnswer(result)
            })

            Log.logMessage(translateQuestion)
            Log.logMessage(result)
            Log.logMessage(f'My Answer: {result[-1]["MyAnswer"]}\nCorrect Answer: {answer[i]}')

            pbar.update()
        
        pbar.close()

        return result