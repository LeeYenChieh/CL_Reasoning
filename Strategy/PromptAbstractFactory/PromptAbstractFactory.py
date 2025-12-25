from Strategy.StrategyType import StrategyType, StrategyNameType

class PromptAbstractFactory:
    def __init__(self):
        pass

    def englishPrompt(self):
        pass

    def chinesePrompt(self):
        pass

    def spanishPrompt(self):
        pass

    def japanesePrompt(self):
        pass

    def russianPrompt(self):
        pass

    def getPrompt(self, type, *args, **kwargs):
        if type == StrategyType.ONLYCHINESE or type == StrategyNameType.ONLYCHINESE:
            return self.chinesePrompt(*args, **kwargs)
        if type == StrategyType.ONLYENGLISH or type == StrategyNameType.ONLYENGLISH:
            return self.englishPrompt(*args, **kwargs)
        if type == StrategyType.ONLYSPANISH or type == StrategyNameType.ONLYSPANISH:
            return self.spanishPrompt(*args, **kwargs)
        if type == StrategyType.ONLYJAPANESE or type == StrategyNameType.ONLYJAPANESE:
            return self.japanesePrompt(*args, **kwargs)
        if type == StrategyType.ONLYRUSSIAN or type == StrategyNameType.ONLYRUSSIAN:
            return self.russianPrompt(*args, **kwargs)
        return None