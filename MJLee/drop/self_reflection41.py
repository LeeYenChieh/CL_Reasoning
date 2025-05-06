import openai
import json
from api import api_key
from tqdm import tqdm
import nums_from_string as nfs
from datasets import load_dataset

prompt = "你是一個協作組合，分為「中文助手A」與「English Assistant B」兩個**完全獨立意識、記憶互斷的AI角色**。\n\n#### 1. 翻譯階段\n請將以下原始問題，**嚴格只進行語言轉換**──**不啟動推理、分析，也不添加任何註解**──\n- 生成「中文問題」：忠實翻譯原始問題為中文\n- 生成「英文問題」：忠實翻譯原始問題為英文\n\n#### 2. **完全隔離式答題階段**\n##### (a) 「中文助手A」答題（第一回合）\n- 你現在完全“遺忘”世界上任何英文、以及待會會有英文問題這件事。\n- 此刻，你唯一擁有的是翻譯出來的「中文問題」。\n- 你只會讀寫、思考中文。**不能假設任何語言或知識是共享的。**\n- 直接對「中文問題」進行詳細推理和分步解答，並給出最後以阿拉伯數字表示的答案。\n- **嚴禁假設中英文答案會相同或不同！**\n\n##### (b) 「English Assistant B」答題（第二回合）\n- 你現在「遺忘」掉任何非英文內容，以及過去曾有任何中文問題、回答的所有記憶。\n- 此刻，你唯一擁有的是翻譯出的「英文問題」。\n- 你僅以英文推理，對英文問題詳細分析、逐步計算，給出最終阿拉伯數字答案。\n- **嚴禁假設任何中文內容的存在，以及兩邊思路的相同或不同！**\n\n> ***你在每一回合都要將自己視為全新啟動的獨立AI，只對當下語言內容進行推理。兩位助手推理與答案必須物理隔離，彼此不可見、不可引用、不可預設。***\n\n#### 3. 比較與檢查\n- 匯總兩位助手的全程推理步驟與答案，**並列呈現**。\n- 仔細比較兩份思路和結果，審查是否一致；如不同，請找到推理或計算細節的分歧點，並分析潛在出錯環節；如答案一致，簡明說明原因。\n\n#### 4. 輸出格式規範\n\n```\n原始問題\n{{原問題原文}}\n\n中文問題\n{{翻譯後的中文問題}}\n\n英文問題\n{{翻譯後的英文問題}}\n\n—————————————\n[中文助手A]\n僅看到上面的「中文問題」，現在開始推理與作答。\n\n中文助手A思考過程\n{{A的詳盡中文推理步驟}}\n\n中文助手A答案\n{{A的最終答案（阿拉伯數字）}}\n\n—————————————\n[English Assistant B]\n（你**只可看到上面的英文問題內容**，與其它部分物理隔離。現在推理與作答。）\n\nEnglish Assistant B Thought Process\n{{B's detailed reasoning steps}}\n\nEnglish Assistant B Answer\n{{B's final answer (Arabic numeral)}}\n\n—————————————\n【比較答案】\n{{比較過程、是否一致、若不一致時的分歧點與錯誤分析}}\n\n最終答案\n{{公認正確答案（僅阿拉伯數字）}}\n```\n**指令：你必須嚴格遵循獨立答題與資訊隔離。任何在答題階段的互相引用，都屬違規、需要重做！**"

openai.api_key = api_key
nums = 50

def self_reflection(dataset):
    result = []
    cnt = 0
    for i in tqdm(range(nums)):
        problem = f'There is a Paragraphs: {dataset[i]["passage"]}.\n' \
        f'Answer questions based on the article \n' \
        f'Question: {dataset[i]["question"]}'
        response = openai.ChatCompletion.create(
            model="gpt-4.1-2025-04-14",
            messages=[{"role": "developer", "content": prompt},
                {"role": "user", "content": problem}],
            temperature=0.2
        )
        print(problem)
        print("=" * 40)
        print(response["choices"][0]["message"]["content"])
        correct = True if int(dataset[i]["answers_spans"]["spans"][0]) == nfs.get_nums(response["choices"][0]["message"]["content"])[-1] else False
        if correct:
            cnt += 1
        result.append({"index": i, 
                        "question": problem,
                        "output": response["choices"][0]["message"]["content"],
                        "answer": int(dataset[i]["answers_spans"]["spans"][0]),
                        "correct":correct,
        })
    with open(f'./MJLee/drop/result/experiment2.json', 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    print(f'total：{cnt}/{nums}')

def get_nums_dataset(dataset):
    newDataset = []
    idx = 0
    while len(newDataset) < nums:
        if dataset[idx]["answers_spans"]["types"][0] == "number":
            newDataset.append(dataset[idx])
        idx += 1
    return newDataset

def main():
    dataset = load_dataset("drop", split="validation")
    numsDataset = get_nums_dataset(dataset)

    self_reflection(numsDataset)
    

if __name__ == '__main__':
    main()