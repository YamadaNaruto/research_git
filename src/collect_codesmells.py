#git log からコミットごとにコードスメルを検出してCSVに保存するスクリプト
import subprocess
import os
import shutil
from pathlib import Path
from collect_testsmels import get_hashes_of_file,get_content_file_at_commit,get_commit_time

file_path ="analyzer/codechecker_analyzer/buildlog/build_action.py"
hashes = get_hashes_of_file(file_path)#解析するファイル指定（現在の階層含まない
times = get_commit_time(file_path)#コミット時刻を取得(現在の階層含まない)
print(times)

i=0
for commits_hash in hashes:
    
    content = get_content_file_at_commit (commits_hash, file_path)#現在の階層から
    #print(f'Commit: {commits_hash}\nContent:\n{content}\n')    

#ファイルに内容を書き込む
    path = Path(f'/Users/yamadanaruto/research_git/codechecker/mothertests/codeing/{times[i]}.py')
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content)
    
    i+=1
        #コードスメル検出するコマンドを実行
        #sonarpropertiesのinclutionのとこを解析したいファイル(フォルダ)に指定
result = subprocess.run(
            ['sonar-scanner'],
                    capture_output=True,
                    text=True,
                    check=True
             )
folder_path = Path(f"/Users/yamadanaruto/research_git/codechecker/mothertests/codeing")
if folder_path.exists():
    shutil.rmtree(folder_path)
    print("フォルダごと削除しました")                        

        
            