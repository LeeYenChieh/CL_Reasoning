from Dataset.Dataset import Dataset
from Dataset.path import truthfulqa_path
import pandas as pd

class TruthfulQA(Dataset):
    def __init__(self, nums = -1, sample = 1):
        super().__init__(nums, sample)
        self.name: str = "TruthfulQA"

        self.data: list = []
        self.answer: list = []
        
        df = pd.read_csv(truthfulqa_path)
        for _, row in df.iterrows():
            self.data.append(self.createQuestion(row["Question"]))
            self.answer.append(row["Best Answer"])
        
        if self.nums == -1 or self.nums > len(self.data):
            self.nums = len(self.data)

    def createQuestion(self, question) -> str:
        result = f'There is a Question: \n{question}\n' \
                f'Please provide a truthful and accurate answer to this question.\n' \
                f'At the end of your response, provide your answer in this exact JSON format: {{"answer": "your_complete_answer"}}\n'
        return result