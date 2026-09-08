from Strategy.PromptAbstractFactory.PromptAbstractFactory import PromptAbstractFactory


class PromptDirectFactory(PromptAbstractFactory):
    """
    A no-Chain-of-Thought prompt (Experiment 4): the model must answer directly.

    This factory is SELF-CONTAINED and must NOT be concatenated with PromptFormatFactory
    (which mandates a "Reasoning process" block). It carries its own compact one-line
    answer-format instruction so that Strategy.parseAnswer can still extract the answer
    from the mandatory {"answer":"..."} line.
    """
    def __init__(self):
        super().__init__()

    def englishPrompt(self, question: str):
        prompt = (
            'For the following question.\n```\n' + question + '\n```\n' +
            '\nAnswer immediately. Do NOT show any reasoning, working, or explanation. If the '
            'question mentions translation, ignore the translation task.\n'
            'Output exactly one line and nothing else:\n'
            '{"answer":"your answer"}\n'
            '(You should not output "your answer" literally. It must strictly follow the rule '
            'required in the question, usually a single English letter or a number. No text '
            'before or after that one JSON line.)\n'
        )
        return prompt

    def chinesePrompt(self, question: str):
        prompt = (
            '對於以下問題\n```\n' + question + '\n```\n' +
            '\n立刻作答。不要輸出任何推理、計算過程或說明。如果題目提到翻譯的字眼，忽略翻譯任務。\n'
            '只輸出一行，不能有其他任何內容：\n'
            '{"answer":"your answer"}\n'
            '（你不該直接輸出 "your answer"，它必須嚴格遵守題目指定的格式，通常是一個英文字母或一個數字。'
            '那一行 JSON 前後不得有其他文字。）\n'
        )
        return prompt

    def spanishPrompt(self, question: str):
        prompt = (
            'Para la siguiente pregunta\n```\n' + question + '\n```\n' +
            '\nResponde de inmediato. NO muestres ningún razonamiento, cálculo ni explicación. Si '
            'la pregunta menciona traducción, ignora la tarea de traducción.\n'
            'Devuelve exactamente una línea y nada más:\n'
            '{"answer":"your answer"}\n'
            '(No debes escribir "your answer" de forma literal. Debe seguir estrictamente la regla '
            'exigida en la pregunta, normalmente una sola letra en inglés o un número. Sin texto '
            'antes ni después de esa línea JSON.)\n'
        )
        return prompt

    def japanesePrompt(self, question: str):
        prompt = (
            '以下の質問について\n```\n' + question + '\n```\n' +
            '\nすぐに回答してください。推論・計算過程・説明は一切出力しないでください。もし質問内で翻訳に'
            'ついて言及されていても、翻訳タスクは無視してください。\n'
            'ちょうど1行だけを出力し、それ以外は何も出力しないでください：\n'
            '{"answer":"your answer"}\n'
            '（"your answer" をそのまま出力してはいけません。質問で要求される規則（通常は英字1文字または'
            '数字）に厳密に従ってください。そのJSON行の前後に他のテキストを入れないでください。）\n'
        )
        return prompt

    def russianPrompt(self, question: str):
        prompt = (
            'Для следующего вопроса\n```\n' + question + '\n```\n' +
            '\nОтвечайте сразу. НЕ показывайте никаких рассуждений, вычислений или пояснений. Если '
            'в вопросе упоминается перевод, игнорируйте задачу перевода.\n'
            'Выведите ровно одну строку и ничего больше:\n'
            '{"answer":"your answer"}\n'
            '(Не выводите "your answer" буквально. Значение должно строго соответствовать правилу '
            'из вопроса, обычно это одна английская буква или число. Никакого текста до или после '
            'этой строки JSON.)\n'
        )
        return prompt
