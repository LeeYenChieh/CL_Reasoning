from Dataset.Dataset import Dataset
from Dataset.path import mgsm_en_path
import json

class MGSM(Dataset):
    NAME = "MGSM"

    def __init__(self, nums=-1, sample=1):
        super().__init__(nums, sample)
        self.name: str = MGSM.NAME

        # 載入 MGSM 數據
        with open(mgsm_en_path, 'r', encoding='utf-8') as f:
            originData = json.load(f)

        self.data: list = []
        self.answer: list = []

        for odata in originData:
            self.data.append(self.createQuestion(odata["question"]))
            # MGSM 取最終數字答案
            self.answer.append(odata.get("answer_number"))

        if self.nums == -1 or self.nums > len(self.data):
            self.nums = len(self.data)

    def createQuestion(self, question: str) -> str:
        """
        生成 prompt，要求模型 step-by-step 解題，最後輸出 JSON 數字答案
        """
        result = (
            f"There is a math word problem:\n"
            f"{question}\n\n"
            f"At the end, provide the final numeric answer in this exact one line JSON format:\n"
            f'{{"answer": "number"}}\n'
            f"The answer must be a single number. You have to output double quotation marks. You have to ouput only one line.\n"
        )
        return result
    
    @staticmethod
    def compareTwoAnswer(answer1: str, answer2: str):
        try:
            if ('.' in answer1 or '.' in answer2) and float(answer1) == float(answer2):
                return True
            elif not ('.' in answer1 or '.' in answer2) and int(answer1) == int(answer2):
                return True
        except:
            return False
        return False
