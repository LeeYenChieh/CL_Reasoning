from Dataset.Dataset import Dataset
from Dataset.path import mathqa_path
import json

class MathQA(Dataset):
    def __init__(self, nums = -1, sample = 1):
        super().__init__(nums, sample)
        self.name: str = "MathQA"

        with open(mathqa_path, 'r') as f:
            originData = json.load(f)
        self.data: list = []
        self.answer:list = []
        for odata in originData:
            self.data.append(self.createQuestion(odata["Problem"], odata["options"]))
            self.answer.append(odata["correct"])
        
        if self.nums == -1 or self.nums > len(self.data):
            self.nums = len(self.data)

    def createQuestion(self, question, choices) -> str:
        result = f'There is a Problem: \n{question}.\n' \
                f'And there are 5 choices\n' \
                f'{choices}\n' \
                f'Please choose a choice based on the question\n' \
                f'At the end of your response, provide your answer in this exact JSON format: {{"answer": "your_letter_choice"}}\n' \
                f'The answer must be a single English letter (a-e).\n'
        return result