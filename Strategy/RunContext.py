from Strategy.Strategy import Strategy

class RunContext():
    def __init__(self):
        self.strategy: Strategy = None
    
    def setStrategy(self, strategy: Strategy):
        self.strategy = strategy
    
    def getStrategyName(self) -> str:
        return self.strategy.getName()
    
    def runExperiment(self) -> list:
        if(not self.strategy):
            print("You need to set strategy first!")
            return
        return self.strategy.getRes()
