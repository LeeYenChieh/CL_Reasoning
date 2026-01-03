from Dataset.Dataset import Dataset
from Dataset.path import mathqa_path
from Dataset.DatasetType import DATASET_TO_NAME, DatasetType
import json

class MathQA(Dataset):
    NAME = DATASET_TO_NAME[DatasetType.MATHQA]

    def __init__(self, nums = -1, sample = 1):
        super().__init__(nums, sample)
        self.name: str = MathQA.NAME

        with open(mathqa_path, 'r') as f:
            originData = json.load(f)

        for idx, odata in enumerate(originData):
            question = self.createQuestion(odata["Problem"], odata["options"])
            ans = odata["correct"]

            self.data.append({
                "id": idx,
                "question": question,
                "answer": ans
            })
        
        if self.nums == -1 or self.nums > len(self.data):
            self.nums = len(self.data)

    def createQuestion(self, question, choices) -> str:
        result = f'There is a Problem: \n{question}.\n' \
                f'And there are 5 choices\n' \
                f'{choices}\n' \
                f'Please choose a choice based on the question\n' \
                f'At the end of your response, provide your answer in this exact JSON format: \n' \
                f'{{"answer": "your_letter_choice"}}\n' \
                f'The answer must be a single English letter (a-e). You have to output double quotation marks. You have to ouput only one line.\n'
        return result