#!/bin/bash

python3 ./main.py --run -m ${1} -d mathqa  -s onlyEnglish --nums 3000
python3 ./main.py --run -m ${1} -d commenseqa -s onlyEnglish --nums 6000
python3 ./main.py --run -m ${1} -d mmlu -s onlyEnglish --nums 6000
python3 ./main.py --run -m ${1} -d truthfulqa -s onlyEnglish --nums 6000
