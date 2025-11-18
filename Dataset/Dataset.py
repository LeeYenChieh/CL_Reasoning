class Dataset():
    def __init__(self, nums: int, sample: int):
        self.name: str = ""
        self.data: list = []
        self.answer: list = []
        self.nums: int = -1 if nums == None else nums
        self.sample: int = 1 if sample == None else sample
    
    @staticmethod
    def compareTwoAnswer(answer1, answer2):
        if answer1 == answer2:
            return True
        return False
    
    def getNums(self) -> int:
        return self.nums
    
    def getSample(self) -> int:
        return self.sample

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