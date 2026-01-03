from Model.Model import Model
from Dataset.Dataset import Dataset
from Strategy.Strategy import Strategy
from Log.Log import Log
from File.File import File
from File.FileFactory import FileFactory
from Strategy.StrategyType import StrategyNameType, NAME_TO_STRATEGY

from Strategy.PromptAbstractFactory.PromptFormatFactory import PromptFormatFactory
from Strategy.PromptAbstractFactory.PromptTwoResultCOTFactory import PromptTwoResultCOTFactory
from Strategy.PromptAbstractFactory.PromptDebateCOTFacroty import PromptDebateCOTFactory

from tqdm import tqdm

class Challenge(Strategy):
    NAME = StrategyNameType.CHALLENGE.value
    def __init__(self, model: Model, dataset: Dataset, log: Log, threshold: int, dataFile1: File, dataFile2: File):
        super().__init__()
        self.name: str = Challenge.NAME
        self.model: Model = model
        self.dataset: Dataset = dataset
        self.log: Log = log
        self.threshold = 3 if threshold == None else threshold
        self.dataFile1 = dataFile1
        self.dataFile2 = dataFile2

        if dataFile1 == None or dataFile2 == None:
            print(f"[{self.name}] Warning: One or both input files are None. Attempting to load default files...")
            self.dataFile1 = FileFactory().getFileByPath(f'result/{model.getName()}_{dataset.getName()}_{StrategyNameType.ONLYCHINESE}.json')
            self.dataFile2 = FileFactory().getFileByPath(f'result/{model.getName()}_{dataset.getName()}_{StrategyNameType.ONLYENGLISH}.json')

            if self.dataFile1 is None:
                raise Exception("[{self.name}] Error: Failed to load default file 1 at {path1}")
                
            else:
                print(f"[{self.name}] Success: Loaded default file 1: {path1}")

            if self.dataFile2 is None:
                raise Exception(f"[{self.name}] Error: Failed to load default file 2 at {path2}")
            else:
                print(f"[{self.name}] Success: Loaded default file 2: {path2}")
        
        self.type1 = NAME_TO_STRATEGY[self.dataFile1.getStrategyName()]
        self.type2 = NAME_TO_STRATEGY[self.dataFile2.getStrategyName()]
        
    def getPrompt(self, type, new_answer):
        prompt = PromptDebateCOTFactory().getPrompt(type, new_answer) + PromptFormatFactory().getPrompt(type)
        return prompt
    
    def cot_Prompt(self, question1, result1, result2):
        prompt = PromptTwoResultCOTFactory().englishPrompt(question1, result1, result2, self.type1, self.type2) \
            + PromptFormatFactory().englishPrompt()
        return prompt
    
    def runChallenge(self, model: Model, dataset: Dataset, question1, question2, result1, result2, answer1, answer2):
        response1, response2 = result1, result2
        answerRecord1, answerRecord2 = [answer1], [answer2]
        record1, record2 = [
            {"role": "user", "content": question1},
            {"role": "assistant", "content": result1}
        ], [
            {"role": "user", "content": question2},
            {"role": "assistant", "content": result2}
        ]

        cur = 0
        while not dataset.compareTwoAnswer(answer1, answer2) and cur < self.threshold:
            prompt1, prompt2 = self.getPrompt(self.type1, response2), self.getPrompt(self.type2, response1)
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

        if self.dataFile1.getNums() < self.dataset.getNums() or self.dataFile1.getSample() != self.dataset.getSample() \
            or self.dataFile2.getNums() < self.dataset.getNums() or self.dataFile2.getSample() != self.dataset.getSample():
            
            raise Exception(f'\nNums or Samples of Data in path1 or path2 doesn\'t match your setting!')


        result = [{
            "Model": self.model.getName(),
            "Dataset": self.dataset.getName(),
            "Strategy": self.name,
            "Data Nums": self.dataset.getNums(),
            "Data Samples": self.dataset.getSample()
        }]

        data1 = self.dataFile1.getData()
        data2 = self.dataFile2.getData()
        different_cnt = 0
        
        for i in range(self.dataset.getDataNums()):
            if data1["id"] != data2["id"]:
                raise Exception(f'[Warning] ID mismatch found at data1 id {data1["id"]} and data2 id {data2["id"]}!')
            datasetData = self.dataset.getDataById(data1["id"])
            if datasetData == None:
                raise Exception(f'[Warning] ID mismatch found at id {data1["id"]}!')

        for i in range(self.dataset.getDataNums()):
            if not self.dataset.compareTwoAnswer(data1[i]["MyAnswer"], data2[i]["MyAnswer"]):
                different_cnt += 1
        self.log.logMessage(f'Different Answer: {different_cnt} / {self.dataset.getDataNums()}')

        pbar = tqdm(total=different_cnt)

        for i in range(self.dataset.getDataNums()):    
            question1, question2, result1, result2 = \
                data1[i]["Translated"], data2[i]["Translated"], data1[i]["Result"], data2[i]["Result"]
            answer1, answer2 = data1[i]["MyAnswer"], data2[i]["MyAnswer"]
            correct_answer = data2[i]["Answer"]

            cur = 0
            resultOutput3 = ""
            myAnswer = ""
            record1, record2 = [], []
            answerRecord1, answerRecord2 = [], []

            if self.dataset.compareTwoAnswer(answer1, answer2):
                myAnswer = answer1

            else:
                record1, record2, answer1, answer2, answerRecord1, answerRecord2, cur = \
                    self.runChallenge(self.model, self.dataset, question1, question2, result1, result2, answer1, answer2) 

                self.log.logMessage(f'Record1：\n{record1}')
                self.log.logMessage(f'結果1：\n{answerRecord1}')
                self.log.logMessage(f'Record2：\n{record2}')
                self.log.logMessage(f'結果2：\n{answerRecord2}')
                self.log.logMessage(f'Times：\n{cur}')

                if self.dataset.compareTwoAnswer(answer1, answer2):
                    myAnswer = answer1

                    self.log.logMessage(f'結果：兩個Agent有相同結果！')
                else:
                    resultOutput3 = self.model.getRes(self.cot_Prompt(question1, result1, result2))
                    myAnswer = self.parseAnswer(resultOutput3)

                    self.log.logMessage(f'結果3：\n{resultOutput3}')

                self.log.logMessage(f'My Answer: {myAnswer}\nCorrect Answer: {correct_answer}')
                pbar.update()

            result.append({
                "Question1": question1,
                "Question2": question2,
                "Record1": record1,
                "Record2": record2,
                "AnswerRecord1": answerRecord1,
                "AnswerRecord2": answerRecord2,
                "Times": cur,
                "Result3": resultOutput3,
                "Answer": correct_answer,
                "MyAnswer": myAnswer
            })
        
        pbar.close()

        return result
    
    @staticmethod
    def getTokenLens(model: Model, data):
        result = model.getTokenLens(data["Question1"]) + model.getTokenLens(data["Question2"])
        for r in data["Record1"]:
            if r["role"] == "assistant":
                result += model.getTokenLens(r["content"]) + model.getTokenLens(r["content"])
        if data["Result3"] != "":
            result += model.getTokenLens(data["Result3"])
        return result