from enum import Enum
from Strategy.Challenge import Challenge as _Challenge

class StrategyType(str, Enum):
    ONLYCHINESE = "onlyChinese"
    ONLYENGLISH = "onlyEnglish"
    ONLYSPANISH = "onlySpanish"
    CHALLENGE = "challenge"
    GETONEOUTPUT = 'getoneresult'

class StrategyNameType(str, Enum):
    ONLYCHINESE = "Only Chinese"
    ONLYENGLISH = "Only English"
    ONLYSPANISH = "Only Spanish"
    CHALLENGE = "Challenge"
    GETONEOUTPUT = "Get One Output"

# 直接取出 value，會是字串
STRATEGY_LIST = [s.value for s in StrategyType]

# 用字串當 key，比較方便查
STRATEGY_TO_NAME = {
    StrategyType.ONLYCHINESE.value: StrategyNameType.ONLYCHINESE.value,
    StrategyType.ONLYENGLISH.value: StrategyNameType.ONLYENGLISH.value,
    StrategyType.ONLYSPANISH.value: StrategyNameType.ONLYSPANISH.value,
    StrategyType.GETONEOUTPUT.value: StrategyNameType.GETONEOUTPUT.value,
    StrategyType.CHALLENGE.value: StrategyNameType.CHALLENGE.value
}

NAME_TO_STRATEGY = {
    StrategyNameType.ONLYCHINESE.value: StrategyType.ONLYCHINESE.value,
    StrategyNameType.ONLYENGLISH.value: StrategyType.ONLYENGLISH.value,
    StrategyNameType.ONLYSPANISH.value: StrategyType.ONLYSPANISH.value,
    StrategyNameType.GETONEOUTPUT.value: StrategyType.GETONEOUTPUT.value,
    StrategyNameType.CHALLENGE.value: StrategyType.CHALLENGE.value
}

STRATEGY_TO_LANGUAGE = {
    StrategyType.ONLYCHINESE.value: 'Chinese',
    StrategyType.ONLYENGLISH.value: 'English',
    StrategyType.ONLYSPANISH.value: 'Spanish',
}