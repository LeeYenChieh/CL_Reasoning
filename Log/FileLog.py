from Log.Log import Log

class FileLog(Log):
    def __init__(self):
        super().__init__()
    
    def logInfo(self, file):
        print('=' * 30)
        print(f'Log Information')
        print(file.getModelName())
        print(file.getDatasetName())
        print(file.getStrategyName())
        print(file.getDataNums())
        print('=' * 30)