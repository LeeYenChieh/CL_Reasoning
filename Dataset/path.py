basedir = './Data/data/'

mathqa_path = basedir + "mathqa.json"
xcopa_path = basedir + "xcopa/data-gmt/zh/test.zh.jsonl"
commensenseqa_path = basedir + "commenseqa.json"
mgsm_en_path = basedir + "mgsm_en.json"
cmb_path = basedir + "CMB/CMB-Exam/CMB-val/CMB-val-merge.json"

translatedBaseDir = './Data/v2_translated'

# English paraphrases produced by Experiment 1 (run_rewrite.py). One file per dataset:
#   {rewrittenBaseDir}/{datasetType}_english.json
rewrittenBaseDir = './Data/rewritten'