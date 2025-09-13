from Dataset.Dataset import Dataset
from Dataset.path import xcopa_path
import json

class XCOPA(Dataset):
    def __init__(self, nums = -1, sample = 1):
        super().__init__(nums, sample)
        self.name: str = "XCOPA"

        self.data: list = []
        self.answer: list = []
        
        with open(xcopa_path, 'r', encoding='utf-8') as f:
            for line in f:
                item = json.loads(line.strip())
                self.data.append(self.createQuestion(item["premise"], item["choice1"], item["choice2"], item["question"]))
                self.answer.append("1" if item["label"] == 0 else "2")
        
        if self.nums == -1 or self.nums > len(self.data):
            self.nums = len(self.data)

    def createQuestion(self, premise, choice1, choice2, question_type) -> str:
        question_word = "cause" if question_type == "cause" else "effect"
        result = f'There is a premise: \n{premise}\n' \
                f'What is the {question_word}?\n' \
                f'Choice 1: {choice1}\n' \
                f'Choice 2: {choice2}\n' \
                f'Please choose the most appropriate choice based on the premise.\n' \
                f'At the end of your response, provide your answer in this exact JSON format: {{"answer": "your_choice_number"}}\n' \
                f'The answer must be either "1" or "2".\n'
        return result