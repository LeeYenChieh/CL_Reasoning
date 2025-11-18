from Strategy.PromptAbstractFactory.PromptAbstractFactory import PromptAbstractFactory
from Strategy.StrategyType import STRATEGY_TO_LANGUAGE

class PromptTwoResultCOTFactory(PromptAbstractFactory):
    def __init__(self):
        super().__init__()

    def englishPrompt(self, question, answer1, answer2, type1, type2):
        return f'For the following question\n```\n{question}\n```\nThere is a {STRATEGY_TO_LANGUAGE[type1]} answer as follows\n' \
            f'```\n{answer1}\n```\n' \
            f'And an {STRATEGY_TO_LANGUAGE[type2]} answer as follows\n' \
            f'```\n{answer2}\n```\n' \
            f'Based on the question, select and output a more correct answer.' \
            f'You must think step by step about which parts of the reasoning in the {STRATEGY_TO_LANGUAGE[type1]} answer and {STRATEGY_TO_LANGUAGE[type2]} answer are incorrect, and output your reasoning process.\n'
    
    def chinesePrompt(self, question, answer1, answer2, type1, type2):
        return f'針對以下問題\n```\n{question}\n```\n有一個 {STRATEGY_TO_LANGUAGE[type1]} 答案如下\n' \
            f'```\n{answer1}\n```\n' \
            f'以及一個 {STRATEGY_TO_LANGUAGE[type2]} 答案如下\n' \
            f'```\n{answer2}\n```\n' \
            f'請根據問題選出並輸出較正確的答案。' \
            f'你必須一步步分析 {STRATEGY_TO_LANGUAGE[type1]} 答案和 {STRATEGY_TO_LANGUAGE[type2]} 答案中推理錯誤的部分，並輸出你的推理過程。\n'

    
    def spanishPrompt(self, question, answer1, answer2, type1, type2):
        return f'Para la siguiente pregunta\n```\n{question}\n```\nHay una respuesta {STRATEGY_TO_LANGUAGE[type1]} como sigue\n' \
            f'```\n{answer1}\n```\n' \
            f'Y una respuesta {STRATEGY_TO_LANGUAGE[type2]} como sigue\n' \
            f'```\n{answer2}\n```\n' \
            f'Basado en la pregunta, selecciona y muestra la respuesta más correcta.' \
            f'Debes pensar paso a paso sobre qué partes del razonamiento en la respuesta {STRATEGY_TO_LANGUAGE[type1]} y la respuesta {STRATEGY_TO_LANGUAGE[type2]} son incorrectas, y mostrar tu proceso de razonamiento.\n'
