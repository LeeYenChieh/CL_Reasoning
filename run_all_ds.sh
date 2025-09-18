#!/bin/bash

models=("deepseek")
datasets=("mathqa")
#("mathqa" "commenseqa" "mgsm" "mmlu" "truthfulqa" "xcopa")
strategies=("multiAgent")
#("onlyChinese" "onlyEnglish" "multiAgent")

mkdir -p logs

for m in "${models[@]}"; do
  for d in "${datasets[@]}"; do
    for s in "${strategies[@]}"; do
      log="logs/${m}_${d}_${s}.log"
      echo "Launching: model=$m dataset=$d strategy=$s | log=$log"
      nohup python3 main.py --run -m "$m" -d "$d" -s "$s" --dirpath result/ --nums 500 > "$log" 2>&1 &
    done
  done
done

echo "All jobs launched in background. Use 'tail -f logs/<file>.log' to monitor."
