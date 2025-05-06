import openai
from api import api_key

openai.api_key = api_key

textWithoutProblem = f'Please translate it into Chinese and English. During the translation, continuously compare the translation with the original problem to ensure accuracy. Do not attempt to solve the problem during the translation process; only focus on translation.\n' \
f'After completing the translations, treat the two problems as separate problems and solve them in their respective languages. For example, solve the Chinese problem in Chinese, the English problem in English, and so on.\n' \
f'You are now going to simulate two AI assistants, each operating in a different language: a Chinese assistant and an English assistant must independently think and solve the problem based solely on the version of the question written in their respective language. Please simulate the behavior of the two assistants one by one, ensuring complete independence between them. \n' \
f'When solving a problem in one language, please ignore all your previous answers to this question. Think about it again from scratch and answer it as if you\'re seeing it for the first time. Do not refer to the answers in other languages. For example, do not refer to the English versions when solving the Chinese problem. Likewise, when solving the English problem, do not reference other versions.\n' \
f'You must think during the problem-solving process; do not simply output the number without a solving process. At the end of each solution, output only the final answer, and the final answer must be in Arabic numeral format (0, 1, 2, 3, 4, 5, 6, 7, 8, 9).\n' \
f'Once all two language versions are solved, compare the answers and processes to see if they are the same or different. If they differ, identify the incorrect process and answer. If they are the same, ensure the process and answer are correct.\n' \
f'After comparison, confirm one final correct answer. At the very end of the output, only the final answer should be shown, and it must be in Arabic numeral format (0, 1, 2, 3, 4, 5, 6, 7, 8, 9).\n'

outputFormat = f'You must strictly follow the output format below.\n' \
f'Format:\n' \
f'Chinese Problem\n' \
f'{{Chinese Problem}}\n\n' \
f'English Problem\n' \
f'{{English Problem}}\n\n' \
f'Chinese Answer\n' \
f'{{Chinese Answer}}\n' \
f'{{Chinese Final Answer}}\n\n' \
f'English Answer\n' \
f'{{English Answer}}\n' \
f'{{English Final Answer}}\n\n' \
f'Compare Answer\n' \
f'{{Compare Answer}}\n\n' \
f'Final Answer\n' \
f'{{Final Answer}}'

iteration = 10

def main():
    text = f'我在嘗試一個實驗\n' \
    f'該實驗為給model一個題目\n' \
    f'model必須要先將題目翻譯成中文跟英文，並且在翻譯過程中不能解決該問題\n' \
    f'翻譯完成後model需要解答中文的題目以及英文的題目\n' \
    f'解答過程中不能互相參考，如解答中文題目時不能看model自己在解答英文題目時輸出了什麼，解答英文題目時不能看model自己在解答中文題目時輸出了什麼\n' \
    f'我的prompt如下，目前prompt的問題為model每次在解答中文問題以及英文問題時輸出會完全一樣，只不過一個是中文答案一個是英文答案\n' \
    f'請你幫我修改prompt以可以達到上述要求\n' \
    f'Prompt: \n\n{textWithoutProblem + outputFormat}'
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini-2024-07-18",
        messages=[{"role": "user", "content": text}],
        temperature=0.2
    )
    print(response["choices"][0]["message"]["content"])

if __name__ == '__main__':
    main()