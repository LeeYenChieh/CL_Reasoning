from argparse import ArgumentParser
import os
import glob
from concurrent.futures import ThreadPoolExecutor, as_completed

from Strategy.RunContext import RunContext
from Strategy.RepairEnglishVariant import RepairEnglishVariant
from Log.NoLog import NoLog
from Log.OneAgentLog import OneAgentLog
from File.File import File


def parseArgs():
    parser = ArgumentParser(description="Repair Experiments 2-4 (rewritten English + prompt style) output files")
    parser.add_argument("--log", action="store_true", help="Enable terminal logging")
    parser.add_argument("--dirpath", required=True, help="Directory containing the evaluation JSON files")
    parser.add_argument("-w", "--workers", type=int, default=3, help="Max concurrent threads/workers")
    return parser.parse_args()


def runRepairTask(file_path, args):
    log = OneAgentLog() if args.log else NoLog()

    try:
        target_file = File(file_path)
    except Exception as e:
        print(f"❌ 無法讀取或解析檔案 {os.path.basename(file_path)}: {e}")
        return file_path, -1

    try:
        # StrategyConfig (languages + promptStyle) and DatasetConfig (useRewrite + language)
        # are reconstructed from the file's own metadata inside RepairEnglishVariant.
        strategy = RepairEnglishVariant(log, target_file)
        context = RunContext()
        context.setStrategy(strategy)
        repaired_ids = context.runExperiment()
        return file_path, (len(repaired_ids) if repaired_ids is not None else -1)
    except Exception as e:
        print(f"❌ 修復檔案 {os.path.basename(file_path)} 時發生錯誤: {e}")
        return file_path, -1


def main():
    args = parseArgs()

    if not os.path.exists(args.dirpath):
        print(f"❌ 找不到目錄: {args.dirpath}")
        return

    files = glob.glob(os.path.join(args.dirpath, "*.json"))
    if not files:
        print(f"⚠️ 在 {args.dirpath} 找不到任何 JSON 檔案。")
        return

    print(f"🚀 準備執行批次修復作業 (English Variant)...")
    print(f"📁 目標資料夾: {args.dirpath}")
    print(f"📄 找到檔案數: {len(files)} 個")
    print(f"⚙️ 執行緒數量: {args.workers}\n")

    with ThreadPoolExecutor(max_workers=args.workers) as executor:
        futures = {executor.submit(runRepairTask, fp, args): fp for fp in files}
        for future in as_completed(futures):
            file_name = os.path.basename(futures[future])
            try:
                _, repaired_count = future.result()
                if repaired_count > 0:
                    print(f"🎉 完美修復！ {file_name} 共計重新推論了 {repaired_count} 筆錯誤紀錄。")
                elif repaired_count == 0:
                    print(f"✨ 檢查完畢！ {file_name} 狀態完美，無需修復。")
                else:
                    print(f"⚠️ 異常警告！ {file_name} 修復程序未正常回傳結果。")
            except Exception as e:
                print(f"❌ 處理 {file_name} 時發生無法預期的例外狀況: {e}")

    print("\n✅ 所有修復作業完成！你可以安心執行算分程式碼 (test_em.py) 了。")


if __name__ == "__main__":
    main()
