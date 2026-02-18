#git log からコミットごとにコードスメルを検出してCSVに保存するスクリプト
import subprocess
import os
from pathlib import Path
from collect_testsmels import get_hashes_of_file,get_content_file_at_commit


hashes = get_hashes_of_file("example_codesmells.py")#解析するファイル指定
base_tmp=Path("/Users/yamadanaruto/Desktop/mothertests")
base_tmp.mkdir(exist_ok=True)
i=0
for commits_hash in hashes:
    
    content = get_content_file_at_commit (commits_hash, 'src/example_codesmells.py')
    #print(f'Commit: {commits_hash}\nContent:\n{content}\n')    

#ファイルに内容を書き込む
    path = f'/Users/yamadanaruto/research_git/src/mothertests/codeing/code_example{i}.py'#書き込む場所
    f = open(path, 'w')
    f.write(content)  
    f.close()
    i+=1
        #コードスメル検出するコマンドを実行
        #sonarpropertiesのinclutionのとこを解析したいファイル(フォルダ)に指定
result = subprocess.run(
            ['sonar-scanner'],
                    capture_output=True,
                    text=True,
                    check=True
             )
                         

        
            