from Strategy.PromptAbstractFactory.PromptAbstractFactory import PromptAbstractFactory

class PromptCOTFactory(PromptAbstractFactory):
    def __init__(self):
        super().__init__()

    def englishPrompt(self, question: str):
        prompt = 'For the following question. \n```\n' + question + '\n```\n' +"\nYou have to solve the question above. You have to think step by step and output your reasoning process. If the question mentions translation, ignore the translation task and focus on the question itself.\n"
        return prompt
    
    def chinesePrompt(self, question: str):
        prompt = '對於以下問題\n```\n' + question + '\n```\n' + "\n你必須解決上述問題。你必須一步一步思考並輸出你的思考過程。如果題目提到翻譯的字眼，忽略翻譯任務，專注在題目上。"
        return prompt
    
    def spanishPrompt(self, question: str):
        prompt = 'Para la siguiente pregunta\n```\n' + question + "\nDebes resolver el problema anterior. Debes pensar paso a paso y mostrar tu proceso de razonamiento. Si la pregunta menciona traducción, ignora la tarea de traducción y concéntrate en el contenido de la pregunta."
        return prompt

    def japanesePrompt(self, question: str):
        prompt = '以下の質問について\n```\n' + question + '\n```\n' + "\n上記の問題を解決してください。ステップバイステップで考え、その思考過程を出力してください。もし質問内で翻訳について言及されていても、翻訳タスクは無視し、問題そのものに集中してください。"
        return prompt

    def russianPrompt(self, question: str):
        prompt = 'Для следующего вопроса\n```\n' + question + '\n```\n' + "\nВы должны решить приведенную выше задачу. Вы должны рассуждать шаг за шагом и вывести ход своих рассуждений. Если в вопросе упоминается перевод, игнорируйте задачу перевода и сосредоточьтесь на самом вопросе."
        return prompt