from Dataset.Dataset import Dataset
from Dataset.path import mmlu_path
import pandas as pd

class MMLU(Dataset):
    def __init__(self, nums = -1, sample = 1):
        super().__init__(nums, sample)
        self.name: str = "MMLU"

        self.data: list = []
        self.answer: list = []
        
        # Load data from CSV file
        df = pd.read_csv(mmlu_path, header=None, names=['question', 'A', 'B', 'C', 'D', 'answer'])
        for _, row in df.iterrows():
            choices = [row['A'], row['B'], row['C'], row['D']]
            self.data.append(self.createQuestion(row['question'], choices))
            self.answer.append(row['answer'].lower())  # Convert to lowercase for consistency
        
        if self.nums == -1 or self.nums > len(self.data):
            self.nums = len(self.data)

    def createQuestion(self, question, choices) -> str:
        choices_str = "\n".join([f"{chr(65+i)}. {choice}" for i, choice in enumerate(choices)])
        result = f'There is a Question: \n{question}\n' \
                f'And there are multiple choices:\n' \
                f'{choices_str}\n' \
                f'Please choose a choice based on the question\n' \
                f'At the end of your response, provide your answer in this exact JSON format: {{"answer": "your_letter_choice"}}\n' \
                f'The answer must be a single English letter (A-D).\n'
        return result