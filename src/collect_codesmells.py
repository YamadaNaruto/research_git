#git log からコミットごとにコードスメルを検出してCSVに保存するスクリプト
import subprocess
import shutil
import time
import requests
import csv
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

file_path = "src/pytest_cases/case_funcs.py"
hashes = get_hashes_of_file(file_path)
times = get_commit_time(file_path)


results = []
prev =None
code_smell_count =get_code_smell_count()
for i, commits_hash in enumerate(hashes):
    content = get_content_file_at_commit(commits_hash, file_path)

    path = Path(f'/Users/yamadanaruto/research_git/python-pytest-cases/mothertests/codeing/{times[i]}.py')#リポジトリ名に変える
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content)

    result = subprocess.run(
        ['sonar-scanner'],
        capture_output=True,
        text=True,
        cwd='/Users/yamadanaruto/research_git/python-pytest-cases'
    )
    if result.returncode != 0:
        print(result.stderr)
        raise subprocess.CalledProcessError(result.returncode, 'sonar-scanner')

    time.sleep(3)  # 解析完了を待つ

    t_code_smell_count = get_code_smell_count()
    if prev is not None:
        code_smell_count = get_code_smell_count()-prev
    prev = t_code_smell_count    

    
    print(f"{times[i]}: code_smells={code_smell_count}")
    clean_time = times[i].strip('"')
    results.append([clean_time, code_smell_count])

folder_path = Path("/Users/yamadanaruto/research_git/python-pytest-cases/mothertests/codeing")#リポ名に変える
if folder_path.exists():
    shutil.rmtree(folder_path)
    print("フォルダごと削除しました")

output_csv = Path("/Users/yamadanaruto/research_git/python-pytest-cases/codesmells.csv")#リポ名に変える
with output_csv.open("w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["date", "code_smells"])
    writer.writerows(results)
print(f"CSVに保存しました: {output_csv}")
