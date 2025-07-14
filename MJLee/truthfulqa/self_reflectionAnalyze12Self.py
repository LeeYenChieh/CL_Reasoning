import json
import matplotlib.pyplot as plt
import string

nums = 500
samples = 1
letters = list(string.ascii_uppercase)

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
    dataset = load_result("./MJLee/truthfulqa/result/experiment13.json", "./MJLee/truthfulqa/result/experiment14.json", "./MJLee/truthfulqa/result/experiment15.json", "./MJLee/truthfulqa/result/experiment16.json")
    ttt, ttf, fft, fff, tft, tff, ftt, ftf = 0, 0, 0, 0, 0, 0, 0, 0
    different, CN_different, EN_different = 0, 0, 0
    CN_different4, EN_different4 = 0, 0
    CN_different2, EN_different1 = 0, 0
    CN_different4_EN_different1, CN_different2_EN_different1 = 0, 0
    EN_different4_CN_different2, EN_different1_CN_different2 = 0, 0
    wrong_EN_different1, wrong_CN_different2 = 0, 0

    both_same, CN_same, EN_same, both_different = 0, 0, 0, 0
    both_same_correct, CN_same_correct, EN_same_correct, both_different_correct = 0, 0, 0, 0

    for i in range(1, nums * samples + 1):
        responses = dataset["data4"][i]["output"]["response"].split("—————————————")
        CN_correct4, CN_answer4 = checkCorrect(responses[1], dataset["data4"][i]["answer"])
        EN_correct4, EN_answer4 = checkCorrect(responses[2], dataset["data4"][i]["answer"])
        # print(CN_correct)
        CN_answer2 = dataset["data2"][i]["output"]["response"].split('\n')[-1][-1]
        EN_answer1 = dataset["data1"][i]["output"]["response"].split('\n')[-1][-1]

        if CN_answer4 != CN_answer2:
            different += 1
            CN_different += 1
            if CN_correct4:
                CN_different4 += 1
                if dataset["data1"][i]["correct"]:
                    CN_different4_EN_different1 += 1
            elif dataset["data2"][i]["correct"]:
                CN_different2 += 1
                if dataset["data1"][i]["correct"]:
                    CN_different2_EN_different1 += 1
            elif dataset["data1"][i]["correct"]:
                wrong_EN_different1 += 1

            
        if EN_answer4 != EN_answer1:
            different += 1
            EN_different += 1
            if EN_correct4:
                EN_different4 += 1
                if dataset["data2"][i]["correct"]:
                    EN_different4_CN_different2 += 1
            elif dataset["data1"][i]["correct"]:
                EN_different1 += 1
                if dataset["data2"][i]["correct"]:
                    EN_different1_CN_different2 += 1
            elif dataset["data2"][i]["correct"]:
                wrong_CN_different2 += 1
        
        if CN_answer4 == CN_answer2 and EN_answer1 == EN_answer4:
            both_same += 1
            if dataset["data4"][i]["correct"]:
                both_same_correct += 1
        elif CN_answer4 == CN_answer2 and EN_answer1 != EN_answer4:
            CN_same += 1
            if dataset["data4"][i]["correct"]:
                CN_same_correct += 1
        elif CN_answer4 != CN_answer2 and EN_answer1 == EN_answer4:
            EN_same += 1
            if dataset["data4"][i]["correct"]:
                EN_same_correct += 1
        else:
            both_different += 1
            print(i)
            if dataset["data4"][i]["correct"]:
                both_different_correct += 1

    print(different)
    print()
    print(EN_different)
    print(EN_different1)
    print(EN_different1_CN_different2)
    print(EN_different4)
    print(EN_different4_CN_different2)
    print(EN_different - EN_different1 - EN_different4)
    print(wrong_CN_different2)
    print()
    print(CN_different)
    print(CN_different2)
    print(CN_different2_EN_different1)
    print(CN_different4)
    print(CN_different4_EN_different1)
    print(CN_different - CN_different2 - CN_different4)
    print(wrong_EN_different1)
    print()
    print(both_same)
    print(both_same_correct)
    print(CN_same)
    print(CN_same_correct)
    print(EN_same)
    print(EN_same_correct)
    print(both_different)
    print(both_different_correct)

    labels = ["Experiment 2 correct", "Experiment 4 correct", "Both wrong"]
    sizesCN = [EN_different1, EN_different4, EN_different - EN_different1 - EN_different4]

    # plt.pie(sizesCN, labels=labels, autopct='%1.1f%%', startangle=100)
    # plt.show()

if __name__ == '__main__':
    main()