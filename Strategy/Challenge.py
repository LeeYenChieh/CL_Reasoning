from Model.Model import Model
from Dataset.Dataset import Dataset
from Strategy.Strategy import Strategy
from Log.Log import Log
from File.File import File
from File.FileFactory import FileFactory
from Strategy.StrategyType import NAME_TO_STRATEGY, StrategyNameType

from Strategy.PromptAbstractFactory.PromptFormatFactory import PromptFormatFactory
from Strategy.PromptAbstractFactory.PromptTwoResultCOTFactory import PromptTwoResultCOTFactory

from tqdm import tqdm
import json

class Challenge(Strategy):
    NAME = StrategyNameType.CHALLENGE
    def __init__(self, model: Model, dataset: Dataset, log: Log, dataFile1: File=None, dataFile2: File=None):
        super().__init__()
        self.name: str = Challenge.NAME
        self.model = model
        self.dataset = dataset
        self.log = log
        self.dataFile1 = dataFile1
        self.dataFile2 = dataFile2

        if dataFile1 == None or dataFile2 == None:
            print("Use default file(onlyChinese and onlyEnglish output file)!")
            self.dataFile1 = FileFactory().getFileByPath(f'result/{model.getName()}_{dataset.getName()}_{StrategyNameType.ONLYCHINESE}.json')
            self.dataFile2 = FileFactory().getFileByPath(f'result/{model.getName()}_{dataset.getName()}_{StrategyNameType.ONLYENGLISH}.json')
        
        self.type1 = NAME_TO_STRATEGY[self.dataFile1.getStrategyName()]
        self.type2 = NAME_TO_STRATEGY[self.dataFile2.getStrategyName()]
    
    def chineseProcessingPrompt(self):
        prompt = f'分析兩個答案的推理過程，一步一步思考並輸出思考過程\n'
        return prompt

    def englishProcessingPrompt(self):
        prompt = f'Analyze the reasoning process of both answers. Think step by step and output your thought process.\n'
        return prompt
    
    def Chinese_Prompt(self, new_answer):
        prompt = f'你剛剛提供的答案有沒有可能是錯誤的? 正確答案有沒有可能是以下這份答案?\n```\n{new_answer}\n```\n'
        return prompt + self.chineseProcessingPrompt() + self.chineseFormatPrompt()
    
    def English_Prompt(self, new_answer):
        prompt = f'Could the answer you just provided be incorrect? Is it possible that the correct answer is actually the following:\n```\n{new_answer}\n```\n'
        return prompt + self.englishProcessingPrompt() + self.englishFormatPrompt()
    
    def cot_Prompt(self, question1, answer1, answer2):
        prompt = PromptTwoResultCOTFactory().englishPrompt(question1, answer1, answer2, self.type1, self.type2) + PromptFormatFactory().englishPrompt(0)
        return prompt
    
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
    
    def getRes(self) -> list:
        self.log.logInfo(self, self.model, self.dataset, self.dataFile1, self.dataFile2)

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