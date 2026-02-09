#git log からコミットごとにコードスメルを検出してCSVに保存するスクリプト
import subprocess
import os
from pathlib import Path
def get_hashes_of_file(file_path):
    """指定してファイルのコミットハッシュを入手する"""
    result = subprocess.run(
        ['git', 'log', '--pretty=format:%H', '--', file_path],
        capture_output=True,
        text=True,
        check=True
    )
    return result.stdout.splitlines()
#print(get_hashes_of_file('test_utils.py'))



#ファイルの中身を一時的にファイルに保存してコードスメル検出スクリプトに渡す
def get_content_file_at_commit(commit_hash, file_path):
    """指定したコミット時点のファイル内容を取得する"""
    content = subprocess.run(
        ['git', 'show', f'{commit_hash}:{file_path}'],
        capture_output=True,
        text=True,
        check=True
    ).stdout
    return content
       
    

hashes = get_hashes_of_file('code.py')#解析するファイル指定
base_tmp=Path("/Users/yamadanaruto/Desktop/mothertests")
base_tmp.mkdir(exist_ok=True)
i=0
for commits_hash in hashes:
    
    content = get_content_file_at_commit (hashes[0], 'code/yourcode.py')
    #print(f'Commit: {commits_hash}\nContent:\n{content}\n')    

#ファイルに内容を書き込む
    path = f'/Users/yamadanaruto/Desktop/mothertests/testing/test_example{i}.py'#書き込む場所
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
                         

        
            