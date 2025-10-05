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
        prompt = f'將以下三個引號內的文字翻譯成中文。翻譯整個問題，包括所有說明和格式要求，絕對不要把要求模型翻譯相關的指令輸出。但是不要提供任何實際的JSON答案 - 只翻譯文字。不要嘗試解決問題，不要推理、分析題目，嚴格只進行語言轉換。\n```\n{question}\n```\n'
        return prompt

    def processPrompt(self) -> str:
        prompt = "\n你必須解決上述問題。你必須一步一步思考並輸出你的思考過程。如果題目提到翻譯的字眼，忽略翻譯任務，專注在題目上。"
        return prompt

    def formatPrompt(self) -> str:
        prompt = f'請嚴格遵守以下格式進行輸出\n' \
            f'推理過程\n' \
            f'{{你的推理過程-注意：**不得重述題目原文或在此加入題目未要求的內容**。}}\n\n' \
            f'最終答案\n' \
            f'{{"answer":"your answer"}}\n' \
            f'（其中 你不該直接輸出"your answer"，"your answer" 應該且必須被取代為題目指定的格式(格式通常是一個英文字母或數字)，整個最終答案區塊只能是那一行 JSON，前後不能有其他文字或說明。）\n'
        return prompt

    def getPrompt(self, question: str) -> str:
        prompt = '對於以下問題\n```\n' + question + '\n```\n' + self.processPrompt() + self.formatPrompt()
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