import json

def main():
    with open(f'./MJLee/result/mgsm/experiment/experiment14.json', 'r') as f:
        result = json.load(f)
    with open(f'./MJLee/result/mgsm/MGSM/mgsm_en_250.json', 'r') as f:
        en = json.load(f)
    with open(f'./MJLee/result/mgsm/gpt4oMGSMOnly/gpt4o_mgsm_zh_250.json', 'r') as f:
        zh = json.load(f)
    
    cnt_zh, cnt_en, cnt_result = 0, 0, 0
    for i in range(250):
        errorString = ""
        if not zh[i]["correct"]:
            errorString += " Chinese"
        else:
            cnt_zh += 1

        if not en[i]["correct"]:
            errorString += " English"
        else:
            cnt_en += 1

        if not result[i]["correct"]:
            errorString += " Final"
        else:
            cnt_result += 1

        if errorString != "":
            print(f'❌ error {errorString} {i}')
    print(f'zh: {cnt_zh}/250')
    print(f'en: {cnt_en}/250')
    print(f'result: {cnt_result}/250')

if __name__ == '__main__':
    main()