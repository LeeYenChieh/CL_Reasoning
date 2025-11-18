from Log.Log import Log

class TwoAgentLog(Log):
    def __init__(self):
        super().__init__()
    
    def logInfo(self, strategy, model, dataset, datafile1, datafile2):
        print('=' * 30)
        print(f'Log Information')
        strategy.printName()
        model.printName()
        model.printTempature()
        dataset.printName()
        dataset.printDataNums()
        print(f'First File Path: {datafile1.getPath()}')
        print(f'Second File Path: {datafile2.getPath()}')
        print('=' * 30)