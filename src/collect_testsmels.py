#git log からコミットごとにテストスメルを検出してCSVに保存するスクリプト
import subprocess
import os
import shutil
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
def get_commit_time(file_path):
    """コミットの時刻を入手する"""
    result = subprocess.run(
        ['git','log','--pretty=format:%ad','--',file_path],
        capture_output=True,
        text=True,
        check=True
    )
    return result.stdout.splitlines()

#ファイルの中身を一時的にファイルに保存してテストスメル検出スクリプトに渡す
def get_content_file_at_commit(commit_hash, file_path):
    """指定したコミット時点のファイル内容を取得する"""
    content = subprocess.run(
        ['git', 'show', f'{commit_hash}:{file_path}'],
        capture_output=True,
        text=True,
        check=True
    ).stdout
    return content
       
def main():
    hashes = get_hashes_of_file('mothertests/testing/test_example0.py')#対象ファイルのパス
    times = get_commit_time('mothertests/testing/test_example0.py')
    print(times)
    i=0
    for commits_hash in hashes:
        
        content = get_content_file_at_commit (commits_hash, 'src/mothertests/testing/test_example0.py')
        #print(f'Commit: {commits_hash}\nContent:\n{content}\n')    

    #ファイルに内容を書き込む
        path = Path(f'/Users/yamadanaruto/Desktop/mothertests/{times[i]}/test_{i}.py')
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content)
        
         
       
            #テストスメル検出するコマンドを実行
        result = subprocess.run(
                    ['python3', '/Users/yamadanaruto/Downloads/PyNose-ASE2022/runner.py'],
                            capture_output=True,
                            text=True,
                            check=True
                    )
        folder_path = Path(f"/Users/yamadanaruto/Desktop/mothertests/{times[i]}")
        if folder_path.exists():
            shutil.rmtree(folder_path)
            print("フォルダごと削除しました")
            i+=1
  
if __name__ == "__main__":
    main()

    


                         

        
            