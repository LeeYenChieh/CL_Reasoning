import openai
import json
from api import api_key
from tqdm import tqdm
import nums_from_string as nfs


openai.api_key = api_key
dir1 = 'mgsm_te'
dir2 = 'mgsm_en'
nums = 250
prompt = "\n請在輸出的最後輸出答案，最後的輸出只能有數字"

def self_reflection(data1, data2, result1, result2):
    result = []
    c1c2, w2c1, w1w2, w1c2 = 0, 0, 0, 0
    c1c2_nums, w2c1_nums, w1w2_nums, w1c2_nums = 0, 0, 0, 0
    for i in tqdm(range(nums)):
        text_for_translation = f'請將"{data1["question"][str(i)]}"翻譯成英文。'
        text_for_compare = f'請比較你輸出的兩個答案並輸出最終的答案。' + prompt
        response_for_trans = openai.ChatCompletion.create(
            model="gpt-4o-mini-2024-07-18",
            messages=[{"role": "user", "content": data1["question"][str(i)] + prompt},
                        {"role": "assistant", "content": result1[i]['output']},
                        {"role": "user", "content": text_for_translation}
                        ],
            temperature=0.2
        )
        response_for_al = openai.ChatCompletion.create(
            model="gpt-4o-mini-2024-07-18",
            messages=[{"role": "user", "content": data1["question"][str(i)] + prompt},
                        {"role": "assistant", "content": result1[i]['output']},
                        {"role": "user", "content": text_for_translation},
                        {"role": "assistant", "content": response_for_trans["choices"][0]["message"]["content"]},
                        {"role": "user", "content": f'請回答"{response_for_trans["choices"][0]["message"]["content"]}"' + prompt}],
            temperature=0.2
        )
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini-2024-07-18",
            messages=[{"role": "user", "content": data1["question"][str(i)] + prompt},
                        {"role": "assistant", "content": result1[i]['output']},
                        {"role": "user", "content": text_for_translation},
                        {"role": "assistant", "content": response_for_trans["choices"][0]["message"]["content"]},
                        {"role": "user", "content": f'請回答"{response_for_trans["choices"][0]["message"]["content"]}"' + prompt},
                        {"role": "assistant", "content": response_for_al["choices"][0]["message"]["content"]},
                        {"role": "user", "content": text_for_compare}],
            temperature=0.2
        )
        correct = True if nfs.get_nums(str(data2['answer'][str(i)]))[-1] == nfs.get_nums(response["choices"][0]["message"]["content"])[-1] else False
        if result1[i]['correct'] and result2[i]['correct']:
            c1c2_nums += 1
            c1c2 += 1 if correct else 0
        elif result1[i]['correct'] and not result2[i]['correct']:
            w2c1_nums += 1
            w2c1 += 1 if correct else 0
        elif not result1[i]['correct'] and not result2[i]['correct']:
            w1w2_nums += 1
            w1w2 += 1 if correct else 0
        else:
            w1c2_nums += 1
            w1c2 += 1 if correct else 0

        result.append({"index": i, 
                        "output_translation": response_for_trans["choices"][0]["message"]["content"],
                        "output_al": response_for_al["choices"][0]["message"]["content"],
                        "output_final": response["choices"][0]["message"]["content"],
                        "answer": data2['answer'][str(i)],
                        "question_translation": text_for_translation,
                        "question_compare": text_for_compare,
                        "correct":correct
        })
    with open(f'./MJLee/result/mgsm/experiment12.json', 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    print(f'wrong in {dir1}, correct in {dir2}：{w1c2_nums}/{nums}')
    print(f'wrong in {dir2}, correct in {dir1}：{w2c1_nums}/{nums}')
    print(f'wrong in {dir1}, wrong in {dir2}：{w1w2_nums}/{nums}')
    print(f'correct in both：{c1c2_nums}/{nums}')
    print()
    print(f'{dir1}：{c1c2_nums + w2c1_nums}/{nums}')
    print(f'{dir2}：{c1c2_nums + w1c2_nums}/{nums}')
    print("-" * 30)
    print("**After self reflection**")
    print(f'wrong in {dir1}, correct in {dir2}：{w1c2}/{w1c2_nums}')
    print(f'wrong in {dir2}, correct in {dir1}：{w2c1}/{w2c1_nums}')
    print(f'wrong in {dir1}, wrong in {dir2}：{w1w2}/{w1w2_nums}')
    print(f'correct in both：{c1c2}/{c1c2_nums}')
    print()
    print(f'total：{c1c2 + w1c2 + w2c1 + w1w2}/{nums}')


def main():
    with open(f'./data/mgsm/{dir1}_{nums}.json', 'r') as f:
        data1 = json.load(f)
    with open(f'./data/mgsm/{dir2}_{nums}.json', 'r') as f:
        data2 = json.load(f)
    with open(f'./MJLee/result/mgsm/{dir1}_{nums}.json', 'r') as f:
        result1 = json.load(f)
    with open(f'./MJLee/result/mgsm/{dir2}_{nums}.json', 'r') as f:
        result2 = json.load(f)

    self_reflection(data1, data2, result1, result2)
    

if __name__ == '__main__':
    main()