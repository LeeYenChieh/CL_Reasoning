from Strategy.Strategy import Strategy
from Model.Model import Model
from Dataset.Dataset import Dataset

class Log():
    def __init__(self):
        pass
    
    def logInfo(self, strategy: Strategy, model: Model, dataset: Dataset):
        pass
    
    def logMessage(self, message: str):
        print('=' * 30)
        print(f'Log: {message}')
        print('=' * 30)