from Strategy.PromptAbstractFactory.PromptAbstractFactory import PromptAbstractFactory

class PromptTranslateFactory(PromptAbstractFactory):
    def __init__(self):
        super().__init__()

    def englishPrompt(self, question: str):
        prompt = f'Translate the text inside the following triple quotation marks into English. Never include the instructions asking the model to perform the translation in the output. If the text is already in English, just output it as-is without any modifications. Translate the entire question including all instructions and format requirements. However, do NOT provide any actual JSON answer - only translate the text. Do not attempt to solve the problem, do not reason or analyze the question, and do not add any comments. Strictly perform language conversion only.\n```\n{question}\n```\n'
        return prompt
    
    def chinesePrompt(self, question: str):
        prompt = f'將以下三個引號內的文字翻譯成中文。翻譯整個問題，包括所有說明和格式要求，絕對不要把要求模型翻譯相關的指令輸出。但是不要提供任何實際的JSON答案 - 只翻譯文字。不要嘗試解決問題，不要推理、分析題目，嚴格只進行語言轉換。\n```\n{question}\n```\n'
        return prompt
    
    def spanishPrompt(self, question: str):
        prompt = f'Traduce al español el texto dentro de las siguientes tres comillas. Traduce toda la pregunta, incluidas todas las instrucciones y los requisitos de formato, pero **no traduzcas el formato JSON**, y **no incluyas en la salida las instrucciones que indican al modelo realizar la traducción**. Pero no proporciones ninguna respuesta JSON real: solo traduce el texto. No intentes resolver el problema, ni razonar, ni analizar la pregunta, estrictamente solo realiza la conversión de idioma.\n```\n{question}\n```\n'
        return prompt
    