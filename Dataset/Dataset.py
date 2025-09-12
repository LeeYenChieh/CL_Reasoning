class Dataset():
    def __init__(self, nums: int = 0, sample: int = 1):
        self.name: str = ""
        self.data: list = []
        self.answer: list = []

        self.nums: int = nums
        if self.nums > len(self.data) or nums == -1:
            self.nums = len(self.data)
        self.sample: int = sample

    def getDataNum(self) -> int:
        return self.nums * self.sample
    
    def getName(self) -> str:
        return self.name

    def getData(self) -> list:
        return self.data[0:self.nums] * self.sample
    
    def getAnswer(self) -> list:
        return self.answer[0:self.nums] * self.sample
    
    def printName(self):
        print(f'Dataset: {self.name}')
        return
    
    def printDataNums(self):
        print(f'Data Nums: {self.nums}')
        print(f'Sample: {self.sample} times')