from Dataset.MMLU import MMLU

d = MMLU(nums=6000)
print(d.getNums())
print(len(d.getData()))
print(len(list(d.type.keys()) ))