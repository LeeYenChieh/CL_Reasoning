from enum import Enum
from Strategy.onlyChinese import OnlyChinese as _OnlyChinese
from Strategy.onlyEnglish import OnlyEnglish as _OnlyEnglish
from Strategy.multiAgent import MultiAgent as _MultiAgent

class StrategyType(str, Enum):
    ONLYCHINESE = "onlyChinese"
    ONLYENGLISH = "onlyEnglish"
    MULTIAGENT = "multiAgent"

    STRATEGY_LIST = [ONLYCHINESE, ONLYENGLISH, MULTIAGENT]
    STRATEGY_NAME_DICT = {
        ONLYCHINESE: _OnlyChinese.NAME,
        ONLYENGLISH: _OnlyEnglish.NAME,
        MULTIAGENT: _MultiAgent.NAME
    }
