import openai
import json
from api import api_key

openai.api_key = api_key
dir1 = 'mgsm_zh'
dir2 = 'mgsm_en'
nums = 250

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

def main():
    with open(f'./data/mgsm/{dir1}_{nums}.json', 'r') as f:
        data1 = json.load(f)
    with open(f'./data/mgsm/{dir2}_{nums}.json', 'r') as f:
        data2 = json.load(f)
    with open(f'./KomaLi/result/mgsm/{dir1}_{nums}.json', 'r') as f:
        result1 = json.load(f)
    with open(f'./KomaLi/result/mgsm/{dir2}_{nums}.json', 'r') as f:
        result2 = json.load(f)

    w1c2, w2c1, w1w2, c1c2 = compute_correct(result1, result2)
    print(w1c2)
    for i in w1c2:
        print(f'問題是 {data1["question"][str(i)]}, 你先前的答案為 {str(result1[i]["simplified"])}，請根據前後文思考問題中各名詞與英文單詞對應的意義後再回答一次並比對兩次的答案並輸出最後的答案')
        text = f'問題是 {data1["question"][str(i)]}, 你先前的答案為 {str(result1[i]["simplified"])}，請根據前後文思考問題中各名詞與英文單詞對應的意義後再回答一次並比對兩次的答案並輸出最後的答案'
        response = openai.ChatCompletion.create(
                model="gpt-4o-mini-2024-07-18",
                messages=[{"role": "user", "content": text}],
            )
        print(response["choices"][0]["message"]["content"])
    # text = f'問題是 {data1['question'][str(7)]}, 你先前的答案為 {result1[7]['answer']}，請翻譯問題成英文後重頭思考英文的問題並再回答一次並比對兩次的答案並輸出最後的答案'
    # response = openai.ChatCompletion.create(
    #         model="gpt-4o-mini-2024-07-18",
    #         messages=[{"role": "user", "content": text}],
    #     )
    # print(response["choices"][0]["message"]["content"])


if __name__ == '__main__':
    main()