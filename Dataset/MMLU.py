from Dataset.Dataset import Dataset
from datasets import load_dataset
from Dataset.DatasetType import DATASET_NAME_DICT, DatasetType
import pandas as pd

class MMLU(Dataset):
    NAME = DATASET_NAME_DICT[DatasetType.MMLU]
    letters = ['A', 'B', 'C', 'D']

    def __init__(self, nums = -1, sample = 1):
        super().__init__(nums, sample)
        self.name: str = MMLU.NAME

        self.data: list = []
        self.answer: list = []
        self.type: dict = {}

        dataset = load_dataset('cais/mmlu', 'all', split='test')
        for data in dataset:
            question = self.createQuestion(data['question'], data['choices'])
            ans = MMLU.letters[data['answer']]

            if not data['subject'] in self.type:
                self.type[data['subject']] = {'question': [], 'answer': []}
            
            self.data.append(question)
            self.answer.append(ans)
            self.type[data['subject']]['question'].append(question)
            self.type[data['subject']]['answer'].append(ans)

        if self.nums == -1 or self.nums > len(self.data):
            self.nums = len(self.data)
        
        self.realData = self.getRealData()
        self.realAnawer = self.getRealAnswer()
        self.nums = len(self.realData)

    def createQuestion(self, question, choices) -> str:
        choicesPrompt = ""

        for i in range(len(choices)):
            choicesPrompt += f'{MMLU.letters[i]}: {choices[i]}\n'

        result = f'There is a Question: \n{question}\n' \
                f'And there are multiple choices:\n' \
                f'{choicesPrompt}\n' \
                f'Please choose a choice based on the question\n' \
                f'At the end of your response, provide your answer in this exact JSON format: \n' \
                f'{{"answer": "your_letter_choice"}}\n' \
                f'The answer must be a single English letter (A-D). You have to output double quotation marks. You have to ouput only one line.\n'
        return result
    
    def getRealData(self):
        types_list = list(self.type.keys()) 
        base = self.nums // len(types_list)       # 每個至少多少
        remainder =  self.nums % len(types_list)   # 剩下多少要分配

        # 先給每個 base，再把餘數加到前面幾個
        eachNums = [base + 1 if i < remainder else base for i in range(len(types_list))]
        result = []
        for n, t in zip(eachNums, types_list):
            result.extend(self.type[t]['question'][0:n])
        return result
    
    def getRealAnswer(self):
        types_list = list(self.type.keys()) 
        base = self.nums // len(types_list)       # 每個至少多少
        remainder =  self.nums % len(types_list)   # 剩下多少要分配

        # 先給每個 base，再把餘數加到前面幾個
        eachNums = [base + 1 if i < remainder else base for i in range(len(types_list))]
        result = []
        for n, t in zip(eachNums, types_list):
            result.extend(self.type[t]['answer'][0:n])
        return result
    
    def getData(self):
        return self.realData * self.sample
    
    def getAnswer(self):
        return self.realAnawer * self.sample