from Model.Model import Model
from Dataset.Dataset import Dataset
from Strategy.Strategy import Strategy
from Log.Log import Log

from tqdm import tqdm

class OnlyChinese(Strategy):
    NAME = "Only Chinese"

    def __init__(self):
        super().__init__()
        self.name: str = OnlyChinese.NAME

    def translatePrompt(self, question: str) -> str:
        prompt = "將以下文字翻譯成中文。翻譯整個問題，包括所有說明和JSON格式要求。但是不要提供任何實際的JSON答案 - 只翻譯文字。不要嘗試解決問題，不要推理、分析題目，嚴格只進行語言轉換。\n\n"
        return prompt + question

    def processPrompt(self) -> str:
        prompt = "\n解決該問題。"
        return prompt

    def formatPrompt(self) -> str:
        prompt = f'請嚴格遵守以下格式進行輸出\n' \
            f'推理過程\n' \
            f'{{你的推理過程}}\n\n' \
            f'最終答案\n' \
            f'{{你的答案，必須完全符合上述問題指定的 JSON 格式，不能添加多餘文字或解釋}}\n'
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