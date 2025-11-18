from Model.Model import Model
from Dataset.Dataset import Dataset
from Strategy.Strategy import Strategy
from Log.Log import Log

from tqdm import tqdm
import json

class CoT(Strategy):
    NAME = "Chain of Thought"
    def __init__(self):
        super().__init__()
        self.name: str = CoT.NAME
    
    def chooseOnePrompt(self, chinese_question, chinese_answer, english_answer):
        prompt = f'對於以下問題\n```\n{chinese_question}\n```\n有一份中文答案如下\n```\n{chinese_answer}\n```\n跟一份英文答案如下\n```\n{english_answer}\n```\n根據問題，選擇並輸出一個較為正確的答案。你必須一步一步思考中文答案與英文答案的推理中哪部分是錯誤的，輸出你的推理過程。\n'
        return prompt
    
    def getPrompt(self, chinese_question, english_question, chinese_answer, english_answer, betterLanguage):
        if len(chinese_answer) > 2048:
            chinese_answer = chinese_answer[0:2048] + '一直重複運算，結束輸出'
        if len(english_answer) > 2048:
            english_answer = english_answer[0:2048] + 'repeatlt compute the same thing, end the output'
        prompt = self.chooseOnePrompt(chinese_question, chinese_answer, english_answer)
        return prompt
    
    def getRes(self, model: Model, dataset: Dataset, log: Log, dataPath1: str=None, dataPath2: str=None, betterLanguage: str='EN') -> list:
        if dataPath1 == None or dataPath2 == None:
            print("Use default file(onlyChinese and onlyEnglish output file)!")
            from Strategy.onlyChinese import OnlyChinese
            from Strategy.onlyEnglish import OnlyEnglish
            dataPath1 = f'result/{model.getName()}_{dataset.getName()}_{OnlyChinese.NAME}.json'
            dataPath2 = f'result/{model.getName()}_{dataset.getName()}_{OnlyEnglish.NAME}.json'

        log.logInfo(self, model, dataset, dataPath1, dataPath2)

        try:
            with open(dataPath1, 'r') as f:
                data1 = json.load(f)
            with open(dataPath2, 'r') as f:
                data2 = json.load(f)
        except:
            log.logMessage(f'\nRead File Error!')
            return []

        if data1[0]["Data Nums"] != dataset.getNums() or data1[0]["Data Samples"] != dataset.getSamples() or data2[0]["Data Nums"] != dataset.getNums() or data2[0]["Data Samples"] != dataset.getSamples():
            log.logMessage(f'\nNums or Samples of Data in path1 or path2 doesn\'t match your setting!')
            return []

        result = [{
            "Model": model.getName(),
            "Dataset": dataset.getName(),
            "Strategy": self.name,
            "Data Nums": dataset.getNums(),
            "Data Samples": dataset.getSamples()
        }]

        pbar = tqdm(total=dataset.getDataNum())
        for i in range(dataset.getDataNum()):
            chinese_question, english_question, chinese_result, english_result = data1[i + 1]["Translated"], data2[i + 1]["Translated"], data1[i + 1]["Result"], data2[i + 1]["Result"]
            chinese_answer, english_answer = data1[i + 1]["MyAnswer"], data2[i + 1]["MyAnswer"]
            correct_answer = data2[i + 1]["Answer"]

            prompt = ""
            resultOutput = ""
            myAnswer = ""

            if dataset.compareTwoAnswer(chinese_answer, english_answer):
                myAnswer = chinese_answer
                # log.logMessage(f'問題：{chinese_question}')
                # log.logMessage(f'結果：兩個Agent有相同結果！')

            else:
                prompt = self.getPrompt(chinese_question, english_question, chinese_result, english_result, betterLanguage)
                resultOutput = model.getRes(prompt)
                myAnswer = self.parseAnswer(resultOutput)
                log.logMessage(f'問題：{chinese_question}')
                log.logMessage(f'Prompt：{prompt}')
                log.logMessage(f'結果：{resultOutput}')
                log.logMessage(f'My Answer: {myAnswer}\nCorrect Answer: {correct_answer}')

            result.append({
                "English Question": english_question,
                "Chinese Question": chinese_question,
                "Prompt": prompt,
                "Result": resultOutput,
                "Answer": correct_answer,
                "MyAnswer": myAnswer
            })

            pbar.update()
        
        pbar.close()

        return result