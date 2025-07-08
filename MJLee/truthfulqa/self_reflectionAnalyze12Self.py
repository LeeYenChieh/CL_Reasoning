import json
import matplotlib.pyplot as plt
import string

def load_result(path1, path2, path3, path4):
    with open(path1, 'r') as f:
        data1 = json.load(f)
    with open(path2, 'r') as f:
        data2 = json.load(f)
    with open(path3, 'r') as f:
        data3 = json.load(f)
    with open(path4, 'r') as f:
        data4 = json.load(f)

    return {
        "data1": data1,
        "data2": data2,
        "data3": data3,
        "data4": data4,
    }

def checkCorrect(response, answer):
    letters = list(string.ascii_uppercase)
    correct = False
    try:
        output = response.split()[-1][-1]
        if output not in letters:
            raise TypeError()
        if answer == output:
            correct = True
    except:
        correct = "true/false"
    return correct, output

def main():
    dataset = load_result("./MJLee/truthfulqa/result/experiment9.json", "./MJLee/truthfulqa/result/experiment10.json", "./MJLee/truthfulqa/result/experiment11_with9_10.json", "./MJLee/truthfulqa/result/experiment12.json")
    ttt, ttf, fft, fff, tft, tff, ftt, ftf = 0, 0, 0, 0, 0, 0, 0, 0
    different, CN_different, EN_different = 0, 0, 0
    for i in range(1, 1501):
        responses = dataset["data4"][i]["output"]["response"].split("—————————————")
        CN_correct, CN_answer = checkCorrect(responses[1], dataset["data4"][i]["answer"])
        EN_correct, EN_answer = checkCorrect(responses[2], dataset["data4"][i]["answer"])

        if dataset["data2"][i]["answer"] != CN_answer:
            different += 1
            CN_different += 1
            print(i)
        if dataset["data1"][i]["answer"] != EN_answer:
            different += 1
            EN_different += 1

    print(different)
    print(EN_different)
    print(CN_different)

if __name__ == '__main__':
    main()