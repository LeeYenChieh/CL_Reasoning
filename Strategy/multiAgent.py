from Model.Model import Model
from Dataset.Dataset import Dataset
from Strategy.Strategy import Strategy
from Log.Log import Log

from tqdm import tqdm
import json

class MultiAgent(Strategy):
    NAME = "Multi Agent"
    def __init__(self):
        super().__init__()
        self.name: str = MultiAgent.NAME
    
    def AC_Wrong_AE_Correct_Prompt(self, chinese_question, chinese_answer, english_answer):
        prompt = f'你剛剛對於以下問題\n```\n{chinese_question}\n```\n的答案是\n```\n{chinese_answer}\n```\n有沒有可能你的答案是錯的，正確答案是\n```\n{english_answer}\n```\n?'
        return prompt
    
    def AE_Wrong_AC_Correct_Prompt(self, english_question, english_answer, chinese_answer):
        prompt = f'The answer you just gave to the following question\n```\n{english_question}\n```\nwas\n```\n{english_answer}\n```\nsomething might be wrong, can the answer be\n```\n{chinese_answer}\n```\n?'
        return prompt
    
    def chooseOnePrompt(self, chinese_question, chinese_answer, english_answer):
        prompt = f'對於以下問題\n```\n{chinese_question}\n```\n有一個中文答案跟一個英文答案，分別是\n```\n{chinese_answer}\n```\n以及\n```\n{english_answer}\n```\n請根據問題挑選出一個比較正確的答案'
        return prompt
    
    def chineseFormatPrompt(self):
        prompt = f'請嚴格遵守以下格式進行輸出\n' \
            f'推理過程\n' \
            f'{{你的推理過程}}\n\n' \
            f'你的回答必須以上述問題中指定的確切JSON格式結束。\n'

        return prompt
    
    def englishFormatPrompt(self):
        prompt = f'Please strictly follow the format below for output\n' \
            f'Reasoning process\n' \
            f'{{your reasoning process}}\n\n' \
            f'Your response must end with the exact JSON format specified in the question above.\n'
        return prompt
    
    def getPrompt(self, chinese_question, english_question, chinese_answer, english_answer):
        prompt1 = self.AC_Wrong_AE_Correct_Prompt(chinese_question, chinese_answer, english_answer) + self.chineseFormatPrompt()
        prompt2 = self.AE_Wrong_AC_Correct_Prompt(english_question, english_answer, chinese_answer) + self.englishFormatPrompt()
        prompt3 = self.chooseOnePrompt(chinese_question, chinese_answer, english_answer) + self.chineseFormatPrompt()
        return prompt1, prompt2, prompt3
    
    def getRes(self, model: Model, dataset: Dataset, log: Log, dataPath1: str=None, dataPath2: str=None) -> list:
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
            chinese_question, english_question, chinese_result, english_result = data1[i + 1]["Translated"], data1[i + 1]["Result"], data2[i + 1]["Translated"], data2[i + 1]["Result"]
            chinese_answer, english_answer = data1[i + 1]["MyAnswer"], data2[i + 1]["MyAnswer"]
            correct_answer = data2[i + 1]["Answer"]

            prompt1, prompt2, prompt3 = "", "", ""
            resultOutput1, resultOutput2, resultOutput3 = "", "", ""
            myAnswer = ""

            if chinese_answer == english_answer:
                myAnswer = chinese_answer

                log.logMessage(f'問題：{chinese_question}')
                log.logMessage(f'結果：兩個Agent有相同結果！')

            else:
                prompt1, prompt2, prompt3 = self.getPrompt(chinese_question, english_question, chinese_result, english_result)
                resultOutput1, resultOutput2 = model.getRes(prompt1), model.getRes(prompt2)
                myResultAnswer1, myResultAnswer2 = self.parseAnswer(resultOutput1), self.parseAnswer(resultOutput2)

                log.logMessage(f'問題：{chinese_question}')
                log.logMessage(f'Prompt1：{prompt1}')
                log.logMessage(f'Prompt2：{prompt2}')
                log.logMessage(f'結果1：{resultOutput1}')
                log.logMessage(f'結果2：{resultOutput2}')

                if myResultAnswer1 == myResultAnswer2:
                    myAnswer = myResultAnswer1

                    log.logMessage(f'結果：兩個Agent有相同結果！')
                else:
                    resultOutput3 = self.parseAnswer(prompt3)
                    myAnswer = self.parseAnswer(resultOutput3)

                    log.logMessage(f'Prompt3：{prompt3}')
                    log.logMessage(f'結果3：{resultOutput3}')

            log.logMessage(f'My Answer: {myAnswer}\nCorrect Answer: {correct_answer}')

            result.append({
                "English Question": english_question,
                "Chinese Question": chinese_question,
                "Prompt1": prompt1,
                "Prompt2": prompt2,
                "Prompt3": prompt3,
                "Result1": resultOutput1,
                "Result2": resultOutput2,
                "Result3": resultOutput3,
                "Answer": correct_answer,
                "MyAnswer": myAnswer
            })

            pbar.update()
        
        pbar.close()

        return result