from Model.Model import Model
from Dataset.Dataset import Dataset
from Strategy.Strategy import Strategy
from Log.Log import Log

from tqdm import tqdm

class OnlyEnglish(Strategy):
    NAME = "Only English"

    def __init__(self, model: Model, dataset: Dataset, log: Log):
        super().__init__()
        self.name: str = OnlyEnglish.NAME
        self.model = model
        self.dataset = dataset
        self.log = log

    def translatePrompt(self, question: str) -> str:
        prompt = f'Translate the text inside the following triple quotation marks into English. Never include the instructions asking the model to perform the translation in the output. If the text is already in English, just output it as-is without any modifications. Translate the entire question including all instructions and format requirements. However, do NOT provide any actual JSON answer - only translate the text. Do not attempt to solve the problem, do not reason or analyze the question, and do not add any comments. Strictly perform language conversion only.\n```\n{question}\n```\n'
        return prompt

    def processPrompt(self) -> str:
        prompt = "\nYou have to solve the question above. You have to think step by step and output your reasoning process. If the question mentions translation, ignore the translation task and focus on the question itself.\n"
        return prompt

    def formatPrompt(self) -> str:
        prompt = f'Please strictly follow the format below for output\n' \
            f'Reasoning process\n' \
            f'{{your reasoning process - Note: **Do not restate the original question text or add content not required by the question**}}\n\n' \
            f'Final Answer\n' \
            f'{{"answer":"your answer"}}\n' \
            f'(You shouldn\'t output "your answer" directly. Where "your answer" must and should strictly follow the rules(Usually a English letter or a number) required in the question. The entire final answer block must only be that one line of JSON, with no extra text or explanation before or after.)\n'
        return prompt

    def getPrompt(self, question: str) -> str:
        prompt = 'For the following question. \n```\n' + question + '\n```\n' + self.processPrompt() + self.formatPrompt()
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
            translateQuestion = self.model.getRes(self.translatePrompt(database[i]))
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
            self.pbar.update()
        
        pbar.close()

        return result