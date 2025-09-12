from Model.Model import Model
from Dataset.Dataset import Dataset
from Strategy.Strategy import Strategy
from Log.Log import Log

from tqdm import tqdm

class OnlyChinese(Strategy):
    def __init__(self):
        super().__init__()
        self.name: str = "Only Chinese"

    def translatePrompt(self, question: str) -> str:
        prompt = "將以下文字翻譯成中文，不要嘗試解決問題，不要推理、分析題目，也不添加任何註解，嚴格只進行語言轉換，不能輸出任何關於答案以及過程的資訊，僅能輸出原本題目的翻譯\n\n"
        return prompt + question

    def processPrompt(self) -> str:
        prompt = "\n解決該問題。"
        return prompt

    def formatPrompt(self) -> str:
        prompt = f'請嚴格遵守以下格式進行輸出\n' \
            f'推理過程\n' \
            f'{{你的推理過程}}\n\n' \
            f'答案\n' \
            f'{{你的答案(只能是一個英文字母)}}\n'
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
            print(database[i])
            print(self.translatePrompt(database[i]))
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