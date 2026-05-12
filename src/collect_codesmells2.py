#git log からコミットごとにコードスメルを検出してCSVに保存するスクリプト
import subprocess
import sys
import json
from datetime import datetime
import shutil
import time
import requests
import csv
import os
from pathlib import Path
from collect_testsmels import get_hashes_of_file,get_content_file_at_commit,get_commit_time

SONAR_URL = "http://localhost:9000"
SONAR_PROJECT_KEY = "detect-codesmells"
TEST_DIRS = []



def get_code_smell_count(k):
    url = f"{SONAR_URL}/api/measures/component_tree"
    params = {
        "component": SONAR_PROJECT_KEY,
        "metricKeys": "code_smells",
        "qualifiers":"FIL",
        "ps": 500
    }
    import os
    token = os.environ.get("SONAR_TOKEN", "")
    response = requests.get(url, params=params, auth=(token, ""), timeout=30)
    data = response.json()
    result = []
    
    for i in range(len(data["components"])):
        name = data["components"][i]["name"]
        date = datetime.strptime(name.replace(".py", "").strip('"'), "%Y-%m-%d %H:%M:%S")
        measures = data["components"][i]["measures"]
        value = measures[0]["value"] if measures else "0"
        result.append([date,int(value)])
    output_csv = Path(f'/Users/yamadanaruto/research_git/add_code_csv/appregated_{k}.csv')
    # output_csv.parent.mkdir(parents=True, exist_ok=True)
    with output_csv.open("w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["date", "code_smells"])
        writer.writerows(result)
        print(f"CSVに保存しました: {output_csv}")
    
    
def main():
    #フォルダづつ処理できるようにする
    k = 0
    folder_name = sys.argv[1]#python3 /Users/yamadanaruto/research_git/src/collect_codesmells2.py python-zeroconf
    repo_root = Path(f'/Users/yamadanaruto/research_git/detectfolder/{folder_name}')
    os.chdir(repo_root)
    folder_path = str(repo_root)#解析するsrcフォルダ
    result = subprocess.run(
                    ['cp', '/Users/yamadanaruto/research_git/src/sonar-project.properties',f'/Users/yamadanaruto/research_git/detectfolder/{folder_name}'],
                            capture_output=True,
                            text=True,
                    )
    if result.returncode != 0:
        print(f"cp エラー:\n{result.stderr}")
    for curdir,dirs,files in os.walk(folder_path):#os.walkを使ってフォルダの中まで検出するように
            #testsフォルダをスキップ
            if os.path.basename(curdir).lower() in ('tests', 'test'):
                test_folder = {
                    'repo_root': str(repo_root),
                    'test_dir': os.path.relpath(curdir, repo_root),
                }
                if test_folder not in TEST_DIRS:
                    TEST_DIRS.append(test_folder)
                print(TEST_DIRS)
                dirs[:] = []             
                continue
            for filename in files:
                #.pyじゃなければスキップ
                if not filename.endswith('.py'):
                    continue
                print(filename)
                file_path = os.path.join(curdir, filename)
                hashes = get_hashes_of_file(file_path)
                times = get_commit_time(file_path)
                i=0
            
                for commits_hash in hashes:
        
                    content = get_content_file_at_commit (commits_hash, file_path)#現在の階層から
                    if content is None:
                        i+=1
                        continue

            #ファイルに内容を書き込む
                    path = Path(f'/Users/yamadanaruto/research_git/detectfolder/{folder_name}/mothertests/codeing/{times[i]}.py')
                    path.parent.mkdir(parents=True, exist_ok=True)
                    path.write_text(content)
                    i+=1
        
                
                try:
                    result = subprocess.run(
                    ['sonar-scanner'],
                            capture_output=True,
                            text=True,
                            check=True,
                            timeout=120
                    )
                except (subprocess.TimeoutExpired, subprocess.CalledProcessError) as e:
                    print(f"スキップ ({e.__class__.__name__}): {filename}")
                    k+=1
                    folder_path = Path(f"/Users/yamadanaruto/research_git/detectfolder/{folder_name}/mothertests/codeing")
                    if folder_path.exists():
                         
                         shutil.rmtree(folder_path)
                         print("フォルダごと削除しました")
                         continue
                time.sleep(3)
                get_code_smell_count(k)
                k+=1

            


                folder_path = Path(f"/Users/yamadanaruto/research_git/detectfolder/{folder_name}/mothertests/codeing")#リポ名に変える
                if folder_path.exists():
                    shutil.rmtree(folder_path)
                    print("フォルダごと削除しました")
   
    tmp_path = Path('/Users/yamadanaruto/research_git/test_dirs.json')
    tmp_path.write_text(json.dumps(TEST_DIRS))

    result = subprocess.run(
                    ['python3', '/Users/yamadanaruto/research_git/src/collect_testsmels2.py', str(tmp_path)],
                            capture_output=True,
                            text=True,
                            cwd=repo_root,
                    )

    if result.returncode != 0:
        print(f"collect_testsmels.py エラー:\n{result.stderr}")
    
if __name__ == '__main__':
    main()
    
