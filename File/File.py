class File():
    def __init__(self, datasetName: str="", modelName: str="", strategyName: str="", nums: int=-1, sample: int=1, data: list=[], path: str=""):
        self.datasetName: str = datasetName
        self.modelName: str = modelName
        self.strategyName: str = strategyName
        self.nums: int = nums
        self.sample: int = sample
        self.dataNums: int = self.nums * self.sample
        self.data: list = data
        self.path: str = path

    def setDatasetName(self, name):
        self.datasetName = name
    
    def setModelName(self, name):
        self.modelName = name
    
    def setStrategyName(self, name):
        self.strategyName = name
    
    def setNums(self, nums):
        self.nums = nums
        self.dataNums = self.nums * self.sample
    
    def setSample(self, samples):
        self.sample = samples
        self.dataNums = self.nums * self.sample
    
    def setData(self, data):
        self.data = data
    
    def setPath(self, path):
        self.path = path
    
    def getDatasetName(self) -> str:
        return self.datasetName
    
    def getModelName(self) -> str:
        return self.modelName
    
    def getNums(self) -> int:
        return self.nums
    
    def getSample(self) -> int:
        return self.sample

    def getStrategyName(self) -> str:
        return self.strategyName
    
    def getDataNums(self) -> int:
        return self.dataNums
    
    def getData(self) -> list:
        return self.data
    
    def getPath(self) -> str:
        return self.path