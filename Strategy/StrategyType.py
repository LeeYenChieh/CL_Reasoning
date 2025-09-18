from enum import Enum
from Strategy.onlyChinese import OnlyChinese as _OnlyChinese
from Strategy.onlyEnglish import OnlyEnglish as _OnlyEnglish
from Strategy.multiAgent import MultiAgent as _MultiAgent

class StrategyType(str, Enum):
    ONLYCHINESE = "onlyChinese"
    ONLYENGLISH = "onlyEnglish"
    MULTIAGENT = "multiAgent"

# 直接取出 value，會是字串
STRATEGY_LIST = [s.value for s in StrategyType]

# 用字串當 key，比較方便查
STRATEGY_NAME_DICT = {
    StrategyType.ONLYCHINESE.value: _OnlyChinese.NAME,
    StrategyType.ONLYENGLISH.value: _OnlyEnglish.NAME,
    StrategyType.MULTIAGENT.value: _MultiAgent.NAME
}
