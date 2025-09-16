from Dataset.Dataset import Dataset
from Dataset.path import truthfulqa_path

from datasets import load_dataset
import string

letters = list(string.ascii_uppercase)

class TruthfulQA(Dataset):
    def __init__(self, nums = -1, sample = 1):
        super().__init__(nums, sample)
        self.name: str = "TruthfulQA"

        self.data: list = []
        self.answer: list = []
        
        dataset = load_dataset("truthfulqa/truthful_qa", "multiple_choice", split="validation")
        
        for data in dataset:
            question = self.createQuestion(data["question"], data["mc1_targets"]["choices"])
            ans = letters[data["mc1_targets"]["labels"].index(1)]

            self.data.append(question)
            self.answer.append(ans)
        
        if self.nums == -1 or self.nums > len(self.data):
            self.nums = len(self.data)


    def createQuestion(self, question, choices):
        choicesPrompt = ""
        
        for i in range(len(choices)):
            choicesPrompt += f'{letters[i]}: {choices[i]}\n'

        prompt = f'There is a Problem: \n{question}.\n' \
        f'And there are {len(choices)} choices\n' \
        f'{choicesPrompt}' \
        f'Please choose a choice based on the question' \
        f'When answering questions, if the problem does not specify considering special cases, always base the answer on real-world situations. If the problem does not specify considering culture, then do not take cultural differences into account when answering; provide an answer that applies universally.\n' \
        f'At the end of your response, provide your answer in this exact JSON format: {{"answer": "your_letter_choice"}}\n' \
        f'The answer must be a single choice and only one English letter (A-Z). You cannot output other letters.'
        return prompt