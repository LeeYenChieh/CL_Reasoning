from Dataset.Dataset import Dataset

class CommenseQA(Dataset):
    def __init__(self, nums = -1, sample = 1):
        super().__init__(nums, sample)
        self.name: str = "CommenseQA"
        self.data: list = []
        self.answer: list = []
        # You should get data and answer here

        if self.nums == -1 or self.nums > len(self.data):
            self.nums = len(self.data)