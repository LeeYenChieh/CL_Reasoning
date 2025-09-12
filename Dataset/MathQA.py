from Dataset.Dataset import Dataset
from Dataset.path import mathqa_path
import json

class MathQA(Dataset):
    def __init__(self, nums = 0, sample = 1):
        super().__init__(nums, sample)
        print(nums)
        self.name: str = "MathQA"

        with open(mathqa_path, 'r') as f:
            originData = json.load(f)
        self.data: list = []
        self.answer:list = []
        for odata in originData:
            self.data.append(self.createQuestion(odata["Problem"], odata["options"]))
            self.answer.append(odata["correct"])

    def createQuestion(self, question, choices) -> str:
        result = f'There is a Problem: \n{question}.\n' \
                f'And there are 5 choices\n' \
                f'{choices}\n' \
                f'Please choose a choice based on the question\n' \
                f'At the end of the output, provide the answer. The answer must be a single choice and only one English letter (a-e). You cannot output other letters.\n'
        return result