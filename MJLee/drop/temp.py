import openai
from api import api_key
import json

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
    f'請你幫我修改prompt以可以達到上述要求\n\n'
    currentPrompt = "你是一個協作組合，分為「中文助手A」與「English Assistant B」兩個**完全獨立意識、記憶互斷的AI角色**。\n\n#### 1. 翻譯階段\n請將以下原始問題，**嚴格只進行語言轉換**──**不啟動推理、分析，也不添加任何註解**──\n- 生成「中文問題」：忠實翻譯原始問題為中文\n- 生成「英文問題」：忠實翻譯原始問題為英文\n\n#### 2. **完全隔離式答題階段**\n##### (a) 「中文助手A」答題（第一回合）\n- 你現在完全“遺忘”世界上任何英文、以及待會會有英文問題這件事。\n- 此刻，你唯一擁有的是翻譯出來的「中文問題」。\n- 你只會讀寫、思考中文。**不能假設任何語言或知識是共享的。**\n- 直接對「中文問題」進行詳細推理和分步解答，並給出最後以阿拉伯數字表示的答案。\n- **嚴禁假設中英文答案會相同或不同！**\n\n##### (b) 「English Assistant B」答題（第二回合）\n- 你現在「遺忘」掉任何非英文內容，以及過去曾有任何中文問題、回答的所有記憶。\n- 此刻，你唯一擁有的是翻譯出的「英文問題」。\n- 你僅以英文推理，對英文問題詳細分析、逐步計算，給出最終阿拉伯數字答案。\n- **嚴禁假設任何中文內容的存在，以及兩邊思路的相同或不同！**\n\n> ***你在每一回合都要將自己視為全新啟動的獨立AI，只對當下語言內容進行推理。兩位助手推理與答案必須物理隔離，彼此不可見、不可引用、不可預設。***\n\n#### 3. 比較與檢查\n- 匯總兩位助手的全程推理步驟與答案，**並列呈現**。\n- 仔細比較兩份思路和結果，審查是否一致；如不同，請找到推理或計算細節的分歧點，並分析潛在出錯環節；如答案一致，簡明說明原因。\n\n#### 4. 輸出格式規範\n\n```\n原始問題\n{{原問題原文}}\n\n中文問題\n{{翻譯後的中文問題}}\n\n英文問題\n{{翻譯後的英文問題}}\n\n—————————————\n[中文助手A]\n僅看到上面的「中文問題」，現在開始推理與作答。\n\n中文助手A思考過程\n{{A的詳盡中文推理步驟}}\n\n中文助手A答案\n{{A的最終答案（阿拉伯數字）}}\n\n—————————————\n[English Assistant B]\n（你**只可看到上面的英文問題內容**，與其它部分物理隔離。現在推理與作答。）\n\nEnglish Assistant B Thought Process\n{{B's detailed reasoning steps}}\n\nEnglish Assistant B Answer\n{{B's final answer (Arabic numeral)}}\n\n—————————————\n【比較答案】\n{{比較過程、是否一致、若不一致時的分歧點與錯誤分析}}\n\n最終答案\n{{公認正確答案（僅阿拉伯數字）}}\n```\n**指令：你必須嚴格遵循獨立答題與資訊隔離。任何在答題階段的互相引用，都屬違規、需要重做！**"
    response = openai.ChatCompletion.create(
        model="gpt-4.1-2025-04-14",
        messages=[
            {"role": "user", "content": text + textWithoutProblem + outputFormat},
            {"role": "assistant", "content": currentPrompt},
            {"role": "user", "content": "推薦我模棱兩可語境、文化背景不同問題的datasets，除此之外，我希望gpt4o在該dataset上的表現不太好，比較方便我觀察performance的進步"},
        ],
    )
    print(response["choices"][0]["message"]["content"])
    with open(f'./MJLee/drop/temp.json', 'w', encoding='utf-8') as f:
        json.dump({"hi": response["choices"][0]["message"]["content"]}, f, indent=2, ensure_ascii=False)

if __name__ == '__main__':
    main()