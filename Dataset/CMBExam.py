from Dataset.Dataset import Dataset
from Dataset.DatasetType import DATASET_NAME_DICT, DatasetType
from Dataset.path import cmb_path
import json

class CMBExam(Dataset):
    NAME = DATASET_NAME_DICT[DatasetType.CMBEXAM]

    def __init__(self, nums = -1, sample = 1):
        super().__init__(nums, sample)
        self.name: str = CMBExam.NAME

        self.data: list = []
        self.answer: list = []
        
        with open(cmb_path, "r") as f:
            dataset = json.load(f)
        
        for data in dataset:
            if len(data["answer"]) != 1:
                continue
            question = self.createQuestion(data["question"], data["option"])
            ans = data["answer"]

            self.data.append(question)
            self.answer.append(ans)
        
        if self.nums == -1 or self.nums > len(self.data):
            self.nums = len(self.data)


    def createQuestion(self, question, choices):
        choicesPrompt = ""
        
        for key, value in choices.items():
            if value:
                choicesPrompt += f'{key}: {value}\n'

        prompt = f'There is a Problem: \n{question}.\n' \
        f'And there are {len(choices)} choices\n' \
        f'{choicesPrompt}' \
        f'Please choose a choice based on the question' \
        f'At the end of your response, provide your answer in this exact JSON format: \n' \
        f'{{"answer": "your_letter_choice"}}\n' \
        f'The answer must be a single choice and only one English letter (A-Z). You cannot output other letters. You have to output double quotation marks. You have to ouput only one line.\n'
        return prompt