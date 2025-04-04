import openai
import json
from api import api_key
from tqdm import tqdm
import nums_from_string as nfs


openai.api_key = api_key
dir1 = 'mgsm_zh'
dir2 = 'mgsm_en'
nums = 250
prompt = "\n請在輸出的最後輸出答案，最後的輸出只能有數字"

def self_reflection(data1, data2, result1, result2):
    result = []
    c1c2, w2c1, w1w2, w1c2 = 0, 0, 0, 0
    c1c2_nums, w2c1_nums, w1w2_nums, w1c2_nums = 0, 0, 0, 0
    for i in tqdm(range(nums)):
        text = text = f'問題是{data2["question"][str(i)]}，請你將題目翻成中文以及英文，一步一步思考，回答中文的問題後回答英文的問題，完成後比較兩個的答案並輸出正確的答案。' + prompt
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini-2024-07-18",
            messages=[{"role": "user", "content": text}],
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
                        "output": response["choices"][0]["message"]["content"],
                        "answer": data2['answer'][str(i)],
                        "question": text,
                        "correct":correct
        })
    with open(f'./MJLee/result/mgsm/experiment11.json', 'w', encoding='utf-8') as f:
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