from Strategy.StrategyType import StrategyType

class PromptAbstractFactory:
    def __init__(self):
        pass

    def englishPrompt(self):
        pass

    def chinesePrompt(self):
        pass

    def spanishPrompt(self):
        pass

    def getPrompt(self, type, *args, **kwargs):
        if type == StrategyType.ONLYCHINESE:
            return self.chinesePrompt(*args, **kwargs)
        if type == StrategyType.ONLYENGLISH:
            return self.englishPrompt(*args, **kwargs)
        if type == StrategyType.ONLYSPANISH:
            return self.spanishPrompt(*args, **kwargs)
        return None