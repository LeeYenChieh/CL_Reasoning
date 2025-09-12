from Log.Log import Log

class OneDatasetLog(Log):
    def __init__(self):
        super().__init__()
    
    def logInfo(self, strategy, model, dataset):
        print(f'Log Information\n')
        strategy.printName()
        model.printName()
        dataset.printName()
        dataset.printDataNums()