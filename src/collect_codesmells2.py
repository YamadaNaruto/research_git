#git log からコミットごとにコードスメルを検出してCSVに保存するスクリプト
import subprocess
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
    response = requests.get(url, params=params, auth=(token, ""))
    data = response.json()
    result = []
    
    for i in range(len(data["components"])):
        name = data["components"][i]["name"]
        date = datetime.strptime(name.replace(".py", "").strip('"'), "%Y-%m-%d %H:%M:%S")
        measures = data["components"][i]["measures"]
        value = measures[0]["value"] if measures else "0"
        result.append([date,int(value)])
    output_csv = Path(f'/Users/yamadanaruto/research_git/src/add_code_csv/appregated_{k}.csv')
    output_csv.parent.mkdir(parents=True, exist_ok=True)
    with output_csv.open("w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["date", "code_smells"])
        writer.writerows(result)
        print(f"CSVに保存しました: {output_csv}")
    
    
  
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
            i=0
          
            for commits_hash in hashes:
    
                content = get_content_file_at_commit (commits_hash, file_path)#現在の階層から
    #print(f'Commit: {commits_hash}\nContent:\n{content}\n')    

        #ファイルに内容を書き込む
                path = Path(f'/Users/yamadanaruto/research_git/{folder_name}/mothertests/codeing/{times[i]}.py')
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(content)
                i+=1
      
               
            result = subprocess.run(
            ['sonar-scanner'],
                    capture_output=True,
                    text=True,
                    check=True
             )
            time.sleep(3)
            get_code_smell_count(k)
            k+=1

           


            folder_path = Path(f"/Users/yamadanaruto/research_git/{folder_name}/mothertests/codeing")#リポ名に変える
            if folder_path.exists():
                shutil.rmtree(folder_path)
                print("フォルダごと削除しました")

           
           
            

result = subprocess.run(
                ['python3', '/Users/yamadanaruto/research_git/src/collect_testsmels.py'],
                        capture_output=True,
                        text=True,
                        check=True
                )     
