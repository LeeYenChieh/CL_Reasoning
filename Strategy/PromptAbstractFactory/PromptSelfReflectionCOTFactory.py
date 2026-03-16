from Strategy.PromptAbstractFactory.PromptAbstractFactory import PromptAbstractFactory

class PromptSelfReflectionCOTFactory(PromptAbstractFactory):
    def __init__(self):
        super().__init__()

    def englishPrompt(self, question, output):
        prompt = f'For the following question:\n' \
            f'```\n{question}\n```\n' \
            f'There is the following answer:\n' \
            f'```\n{output}\n```\n' \
            f'Check if the answer has any errors. If there are errors, point them out and correct them. Regardless of whether there are errors or not, output a final answer.'
        return prompt  

    def chinesePrompt(self, question, output):
        prompt = f'對於下面的問題\n' \
            f'```\n{question}\n```\n' \
            f'有一份下面的回答\n' \
            f'```\n{output}\n```\n' \
            f'確認回答是否有錯誤，如果有錯誤，指出來並修正，無論是否有錯誤，都要輸出一份最終答案'
        return prompt
    
    def spanishPrompt(self, question, output):
        prompt = f'Para la siguiente pregunta:\n' \
            f'```\n{question}\n```\n' \
            f'Existe la siguiente respuesta:\n' \
            f'```\n{output}\n```\n' \
            f'Comprueba si la respuesta tiene algún error. Si hay errores, señálalos y corrígelos. Independientemente de si hay errores o no, debes emitir una respuesta final.'
        return prompt

    def japanesePrompt(self, question, output):
        prompt = f'以下の質問に対して、\n' \
            f'```\n{question}\n```\n' \
            f'以下の回答があります。\n' \
            f'```\n{output}\n```\n' \
            f'回答に間違いがあるか確認してください。間違いがある場合は、それを指摘して修正してください。間違いの有無にかかわらず、最終的な回答を出力してください。'
        return prompt

    def russianPrompt(self, question, output):
        prompt = f'Для следующего вопроса:\n' \
            f'```\n{question}\n```\n' \
            f'Существует следующий ответ:\n' \
            f'```\n{output}\n```\n' \
            f'Проверьте, есть ли в ответе ошибки. Если есть ошибки, укажите на них и исправьте. Независимо от того, есть ошибки или нет, необходимо вывести окончательный ответ.'
        return prompt