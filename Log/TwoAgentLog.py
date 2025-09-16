from Log.Log import Log

class TwoAgentLog(Log):
    def __init__(self):
        super().__init__()
    
    def logInfo(self, strategy, model, dataset, datapath1, datapath2):
        print('=' * 30)
        print(f'Log Information')
        strategy.printName()
        model.printName()
        dataset.printName()
        dataset.printDataNums()
        print(f'First File Path: {datapath1}')
        print(f'Second File Path: {datapath2}')
        print('=' * 30)