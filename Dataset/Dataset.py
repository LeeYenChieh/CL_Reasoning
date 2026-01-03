class Dataset():
    def __init__(self, nums: int, sample: int):
        self.name: str = "Dataset"
        self.data: list[dict] = []

        if nums is None:
            print(f"[{self.name}] Notice: 'nums' is None. Defaulting to -1 (Use all data).")
            self.nums = -1
        else:
            self.nums = nums
            print(f"[{self.name}] Log: 'nums' set to {self.nums}.")

        # 處理 sample 的 None 判斷與 Log
        if sample is None:
            print(f"[{self.name}] Notice: 'sample' is None. Defaulting to 1.")
            self.sample = 1
        else:
            self.sample = sample
            print(f"[{self.name}] Log: 'sample' set to {self.sample}.")
    
    @staticmethod
    def compareTwoAnswer(answer1, answer2):
        if answer1 == answer2:
            return True
        return False
    
    def getNums(self) -> int:
        return self.nums
    
    def getSample(self) -> int:
        return self.sample

    def getDataNums(self) -> int:
        return self.nums * self.sample
    
    def getName(self) -> str:
        return self.name

    def getData(self) -> list:
        return self.data[0:self.nums] * self.sample
    
    def getDataById(self, id: int):
        if id >= self.getNums:
            return None
        return self.data[id]
        
    def printName(self):
        print(f'Dataset: {self.name}')
        return
    
    def printDataNums(self):
        print(f'Data Nums: {self.nums}')
        print(f'Sample: {self.sample} times')