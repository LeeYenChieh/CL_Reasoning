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

def compute_correct(result1, result2):
    w1c2 = []
    w2c1 = []
    w1w2 = []
    c1c2 = []
    for i in range(nums):
        if result1[i]['correct'] and result2[i]['correct']:
            c1c2.append(i)
        elif result1[i]['correct'] and not result2[i]['correct']:
            w2c1.append(i)
        elif not result1[i]['correct'] and not result2[i]['correct']:
            w1w2.append(i)
        else:
            w1c2.append(i)
    print(f'wrong in {dir1}, correct in {dir2}：{len(w1c2)}/{nums}')
    print(f'wrong in {dir2}, correct in {dir1}：{len(w2c1)}/{nums}')
    print(f'wrong in {dir1}, wrong in {dir2}：{len(w1w2)}/{nums}')
    print(f'correct in both：{len(c1c2)}/{nums}')
    return w1c2, w2c1, w1w2, c1c2

def self_reflection(index, w_dir, c_dir, w_data, c_data, w_result, c_result):
    result = []
    cnt = 0
    bar = tqdm(total=len(index))
    for i in index:
        text = f'問題是{w_data["question"][str(i)]}，請你將題目翻成中文以及英文，分別回答一次後比較兩個的答案並輸出正確的答案。' + prompt
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini-2024-07-18",
            messages=[{"role": "user", "content": text}],
            temperature=0.2
        )
        correct = True if nfs.get_nums(str(w_data['answer'][str(i)]))[-1] == nfs.get_nums(response["choices"][0]["message"]["content"])[-1] else False
        if correct:
            cnt += 1
        result.append({"index": i, 
                        "output": response["choices"][0]["message"]["content"],
                        "answer": w_data['answer'][str(i)],
                        "question": text,
                        "correct":correct
        })
        bar.update(1)
    with open(f'./MJLee/result/mgsm/w_{w_dir}_c_{c_dir}_{nums}.json', 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    print(f'wrong in {w_dir}, correct in {c_dir} after self reflection：{cnt}/{len(index)}')



def main():
    with open(f'./data/mgsm/{dir1}_{nums}.json', 'r') as f:
        data1 = json.load(f)
    with open(f'./data/mgsm/{dir2}_{nums}.json', 'r') as f:
        data2 = json.load(f)
    with open(f'./MJLee/result/mgsm/{dir1}_{nums}.json', 'r') as f:
        result1 = json.load(f)
    with open(f'./MJLee/result/mgsm/{dir2}_{nums}.json', 'r') as f:
        result2 = json.load(f)

    w1c2, w2c1, w1w2, c1c2 = compute_correct(result1, result2)
    self_reflection(w1c2, dir1, dir2, data1, data2, result1, result2)
    self_reflection(w2c1, dir2, dir1, data2, data1, result2, result1)

if __name__ == '__main__':
    main()