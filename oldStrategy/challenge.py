from Model.Model import Model
from Dataset.Dataset import Dataset
from Strategy.Strategy import Strategy
from Log.Log import Log

from tqdm import tqdm
import json

class Challenge(Strategy):
    NAME = "Challenge"
    def __init__(self):
        super().__init__()
        self.name: str = Challenge.NAME
    
    def chineseProcessingPrompt(self):
        prompt = f'分析兩個答案的推理過程，一步一步思考並輸出思考過程\n'
        return prompt

    def englishProcessingPrompt(self):
        prompt = f'Analyze the reasoning process of both answers. Think step by step and output your thought process.\n'
        return prompt
    
    def chineseFormatPrompt(self):
        prompt = f'請嚴格遵守以下格式進行輸出\n' \
            f'推理過程\n' \
            f'{{你的推理過程-注意：**不得重述題目原文或在此加入題目未要求的內容**。}}\n\n' \
            f'最終答案\n' \
            f'{{"answer":"your answer"}}\n' \
            f'（其中 你不該直接輸出"your answer"，"your answer" 應該且必須被取代為題目指定的格式(格式通常是一個英文字母或數字)，整個最終答案區塊只能是那一行JSON，前後不能有其他文字或說明。）\n'
        return prompt

    def englishFormatPrompt(self):
        prompt = f'Please strictly follow the format below for output\n' \
            f'Reasoning process\n' \
            f'{{your reasoning process - Note: **Do not restate the original question text or add content not required by the question**}}\n\n' \
            f'Final Answer\n' \
            f'{{"answer":"your answer"}}\n' \
            f'(You shouldn\'t output "your answer" directly. Where "your answer" must and should strictly follow the rules(Usually a English letter or a number) required in the question. The entire final answer block must only be that one line of JSON, with no extra text or explanation before or after.)\n'
        return prompt
    
    def Chinese_Prompt(self, new_answer):
        prompt = f'你剛剛提供的答案有沒有可能是錯誤的? 正確答案有沒有可能是以下這份答案?\n```\n{new_answer}\n```\n'
        return prompt + self.chineseProcessingPrompt() + self.chineseFormatPrompt()
    
    def English_Prompt(self, new_answer):
        prompt = f'Could the answer you just provided be incorrect? Is it possible that the correct answer is actually the following:\n```\n{new_answer}\n```\n'
        return prompt + self.englishProcessingPrompt() + self.englishFormatPrompt()
    
    def cot_Prompt(self, chinese_question, chinese_answer, english_answer):
        prompt = f'For the following question\n```\n{chinese_question}\n```\nThere is a Chinese answer as follows\n```\n{chinese_answer}\n```\nAnd an English answer as follows\n```\n{english_answer}\n```\nBased on the question, select and output a more correct answer. You must think step by step about which parts of the reasoning in the Chinese answer and English answer are incorrect, and output your reasoning process.\n'
        return prompt + self.englishProcessingPrompt() + self.englishFormatPrompt()
    
    def runChallenge(self, model: Model, dataset: Dataset, chinese_question, english_question, chinese_result, english_result, chinese_answer, english_answer, threshold=3):
        response1, response2 = chinese_result, english_result
        answer1, answer2 = chinese_answer, english_answer
        answerRecord1, answerRecord2 = [answer1], [answer2]
        record1, record2 = [{"role": "user", "content": chinese_question}, {"role": "assistant", "content": chinese_result}], [{"role": "user", "content": english_question}, {"role": "assistant", "content": english_result}]
        cur = 0
        while not dataset.compareTwoAnswer(answer1, answer2) and cur < threshold:
            prompt1, prompt2 = self.Chinese_Prompt(response2), self.English_Prompt(response1)
            record1.append({"role": "user", "content": prompt1})
            record2.append({"role": "user", "content": prompt2})
            response1, response2 = model.getListRes(record1), model.getListRes(record2)
            record1.append({"role": "assistant", "content": response1})
            record2.append({"role": "assistant", "content": response2})
            answer1, answer2 = self.parseAnswer(response1), self.parseAnswer(response2)
            answerRecord1.append(answer1)
            answerRecord2.append(answer2)

            cur += 1
        return record1, record2, answer1, answer2, answerRecord1, answerRecord2, cur
    
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
            chinese_question, english_question, chinese_result, english_result = data1[i + 1]["Translated"], data2[i + 1]["Translated"], data1[i + 1]["Result"], data2[i + 1]["Result"]
            chinese_answer, english_answer = data1[i + 1]["MyAnswer"], data2[i + 1]["MyAnswer"]
            correct_answer = data2[i + 1]["Answer"]

            cur = 0
            resultOutput3 = ""
            myAnswer = ""
            record1, record2 = [], []
            answerRecord1, answerRecord2 = [], []

            if dataset.compareTwoAnswer(chinese_answer, english_answer):
                myAnswer = chinese_answer

            else:
                record1, record2, answer1, answer2, answerRecord1, answerRecord2, cur = self.runChallenge(model, dataset, chinese_question, english_question, chinese_result, english_result, chinese_answer, english_answer) 

                log.logMessage(f'Record1：\n{record1}')
                log.logMessage(f'結果1：\n{answerRecord1}')
                log.logMessage(f'Record2：\n{record2}')
                log.logMessage(f'結果2：\n{answerRecord2}')
                log.logMessage(f'Times：\n{cur}')

                if dataset.compareTwoAnswer(answer1, answer2):
                    myAnswer = answer1

                    log.logMessage(f'結果：兩個Agent有相同結果！')
                else:
                    resultOutput3 = model.getRes(self.cot_Prompt(chinese_question, chinese_answer, english_answer))
                    myAnswer = self.parseAnswer(resultOutput3)

                    log.logMessage(f'結果3：\n{resultOutput3}')

                log.logMessage(f'My Answer: {myAnswer}\nCorrect Answer: {correct_answer}')

            result.append({
                "English Question": english_question,
                "Chinese Question": chinese_question,
                "Record1": record1,
                "Record2": record2,
                "AnswerRecord1": answerRecord1,
                "AnswerRecord2": answerRecord2,
                "Times": cur,
                "Result3": resultOutput3,
                "Answer": correct_answer,
                "MyAnswer": myAnswer
            })

            pbar.update()
        
        pbar.close()

        return result