from Strategy.PromptAbstractFactory.PromptAbstractFactory import PromptAbstractFactory

class PromptSelfReflectionCOTFactory(PromptAbstractFactory):
    def __init__(self):
        super().__init__()

    def englishPrompt(self):
        prompt = f'Review your previous answer. If there are any errors, point them out and correct them. Then, regardless of whether there were errors or not, output the final answer.\n'
        return prompt    

    def chinesePrompt(self):
        prompt = f'重新審視你先前的答案，如果有錯誤的話指出來並修正，接著不管有沒有錯誤，都把最終答案輸出\n'
        return prompt
    
    def spanishPrompt(self):
        prompt = f'Revisa tu respuesta anterior. Si hay algún error, señálalo y corrígelo. Luego, independientemente de si hubo errores o no, genera la respuesta final.\n'
        return prompt

    def japanesePrompt(self):
        prompt = f'以前の回答を再確認してください。もし間違いがあれば指摘して修正してください。その後、間違いの有無にかかわらず、最終的な回答を出力してください。\n'
        return prompt

    def russianPrompt(self):
        prompt = f'Пересмотрите свой предыдущий ответ. Если есть какие-либо ошибки, укажите на них и исправьте. Затем, независимо от того, были ли ошибки, выведите окончательный ответ.\n'
        return prompt