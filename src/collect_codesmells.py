#git log からコミットごとにコードスメルを検出してCSVに保存するスクリプト
import subprocess
import shutil
import time
import requests
import csv
import os
from pathlib import Path
from collect_testsmels import get_hashes_of_file,get_content_file_at_commit,get_commit_time

SONAR_URL = "http://localhost:9000"
SONAR_PROJECT_KEY = "detect-codesmells"

def get_code_smell_count():
    url = f"{SONAR_URL}/api/measures/component"
    params = {
        "component": SONAR_PROJECT_KEY,
        "metricKeys": "code_smells"
    }
    import os
    token = os.environ.get("SONAR_TOKEN", "")
    response = requests.get(url, params=params, auth=(token, ""))
    response.raise_for_status()
    measures = response.json()["component"]["measures"]
    if not measures:
        return 0
    return int(measures[0]["value"])
#フォルダづつ処理できるようにする
k=0
folder_name = "picrust2"#このリポジトリ名
folder_path = "/Users/yamadanaruto/research_git/picrust2/scripts"#解析するsrcフォルダ
for curdir,dirs,files in os.walk(folder_path):#os.walkを使ってフォルダの中まで検出するように
        for filename in files:
            #.pyじゃなければスキップ
            if not filename.endswith('.py'):
                continue
            print(filename)
            file_path = os.path.join(curdir, filename)
            hashes = get_hashes_of_file(file_path)
            times = get_commit_time(file_path)


            results = []
            temp_dir = Path(f'/Users/yamadanaruto/research_git/{folder_name}/mothertests/codeing')
            temp_file = temp_dir / 'target.py'  # 毎回同じファイル名で上書き
            temp_dir.mkdir(parents=True, exist_ok=True)
            for i, commits_hash in enumerate(hashes):
                content = get_content_file_at_commit(commits_hash, file_path)
                if content is None:
                    continue
                temp_file.write_text(content)

                result = subprocess.run(
                    ['sonar-scanner'],
                    capture_output=True,
                    text=True,
                    cwd=f'/Users/yamadanaruto/research_git/{folder_name}'
                )
                if result.returncode != 0:
                    print(result.stderr)
                    raise subprocess.CalledProcessError(result.returncode, 'sonar-scanner')

                time.sleep(3)  # 解析完了を待つ

                code_smell_count = get_code_smell_count()

                print(f"{times[i]}: code_smells={code_smell_count}")
                clean_time = times[i].strip('"')
                results.append([clean_time, code_smell_count])

            folder_path = Path(f"/Users/yamadanaruto/research_git/{folder_name}/mothertests/codeing")#リポ名に変える
            if folder_path.exists():
                shutil.rmtree(folder_path)
                print("フォルダごと削除しました")

            output_csv = Path(f'/Users/yamadanaruto/research_git/src/add_code_csv/appregated_{k}.csv')#リポ名に変える
            with output_csv.open("w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(["date", "code_smells"])
                writer.writerows(results)
            print(f"CSVに保存しました: {output_csv}")
            k+=1
result = subprocess.run(
                ['python3', '/Users/yamadanaruto/research_git/src/collect_testsmels.py'],
                        capture_output=True,
                        text=True,
                        check=True
                )     
