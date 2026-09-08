from Strategy.PromptAbstractFactory.PromptAbstractFactory import PromptAbstractFactory


class PromptShortCOTFactory(PromptAbstractFactory):
    """
    A terser Chain-of-Thought reasoning prompt (Experiment 3).

    Mirrors PromptCOTFactory, but asks the model to keep its reasoning to only a few short
    steps. It is meant to be concatenated with PromptFormatFactory, so the final output
    format stays identical to the standard CoT run and remains parseable by
    Strategy.parseAnswer.
    """
    def __init__(self):
        super().__init__()

    def englishPrompt(self, question: str):
        prompt = (
            'For the following question. \n```\n' + question + '\n```\n' +
            '\nYou have to solve the question above. Think briefly: use at most 2-3 short '
            'reasoning steps, then stop and give the answer. If the question mentions '
            'translation, ignore the translation task and focus on the question itself.\n'
        )
        return prompt

    def chinesePrompt(self, question: str):
        prompt = (
            '對於以下問題\n```\n' + question + '\n```\n' +
            '\n你必須解決上述問題。請簡短思考：最多使用 2 至 3 個簡短的推理步驟，然後停止並給出答案。'
            '如果題目提到翻譯的字眼，忽略翻譯任務，專注在題目上。'
        )
        return prompt

    def spanishPrompt(self, question: str):
        prompt = (
            'Para la siguiente pregunta\n```\n' + question + '\n```\n' +
            '\nDebes resolver el problema anterior. Piensa de forma breve: usa como máximo 2 o 3 '
            'pasos de razonamiento cortos y luego detente y da la respuesta. Si la pregunta '
            'menciona traducción, ignora la tarea de traducción y concéntrate en el contenido de '
            'la pregunta.'
        )
        return prompt

    def japanesePrompt(self, question: str):
        prompt = (
            '以下の質問について\n```\n' + question + '\n```\n' +
            '\n上記の問題を解決してください。簡潔に考えてください。推論のステップは多くても2〜3個の短い'
            'ものにとどめ、その後は止めて答えを出してください。もし質問内で翻訳について言及されていても、'
            '翻訳タスクは無視し、問題そのものに集中してください。'
        )
        return prompt

    def russianPrompt(self, question: str):
        prompt = (
            'Для следующего вопроса\n```\n' + question + '\n```\n' +
            '\nВы должны решить приведённую выше задачу. Рассуждайте кратко: используйте не более '
            '2–3 коротких шагов рассуждения, затем остановитесь и дайте ответ. Если в вопросе '
            'упоминается перевод, игнорируйте задачу перевода и сосредоточьтесь на самом вопросе.'
        )
        return prompt
