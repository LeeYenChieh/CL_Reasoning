from enum import Enum
from Strategy.onlyChinese import OnlyChinese as _OnlyChinese
from Strategy.onlyEnglish import OnlyEnglish as _OnlyEnglish
from Strategy.onlySpanish import OnlySpanish as _OnlySpanish
from Strategy.multiAgent import MultiAgent as _MultiAgent
from Strategy.chooseAnswer import ChooseAnswer as _ChooseAnswer
from Strategy.getOneOutput import GetOneOutput as _GetOneResult
from Strategy.basic import Basic as _Basic
from Strategy.cot import CoT as _CoT
from Strategy.Challenge import Challenge as _Challenge

class StrategyType(str, Enum):
    ONLYCHINESE = "onlyChinese"
    ONLYENGLISH = "onlyEnglish"
    ONLYSPANISH = "onlySpanish"
    MULTIAGENT = "multiAgent"
    CHOOSEANSWER = "chooseanswer"
    GETONEOUTPUT = 'getoneresult'
    BASIC = "basic"
    COT = "cot"
    CHALLENGE = "challenge"

# 直接取出 value，會是字串
STRATEGY_LIST = [s.value for s in StrategyType]

# 用字串當 key，比較方便查
STRATEGY_NAME_DICT = {
    StrategyType.ONLYCHINESE.value: _OnlyChinese.NAME,
    StrategyType.ONLYENGLISH.value: _OnlyEnglish.NAME,
    StrategyType.ONLYSPANISH.value: _OnlySpanish.NAME,
    StrategyType.MULTIAGENT.value: _MultiAgent.NAME,
    StrategyType.CHOOSEANSWER.value: _ChooseAnswer.NAME,
    StrategyType.GETONEOUTPUT.value: _GetOneResult.NAME,
    StrategyType.BASIC.value: _Basic.NAME,
    StrategyType.COT.value: _CoT.NAME,
    StrategyType.CHALLENGE.value: _Challenge.NAME
}
