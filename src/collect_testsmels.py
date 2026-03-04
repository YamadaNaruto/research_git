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
        ['git','log','--pretty=format:%ad','--date=format:"%Y-%m-%d %H:%M:%S"','--',file_path],
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
    #フォルダを読み込んでファイルを取得
    folder_path = "src/mothertests/testing"
    for filename in os.listdir(folder_path):
        
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path):
            print(filename);    
            hashes = get_hashes_of_file(file_path)#対象ファイルのパス(現在の階層含まないスラッシュなし)
            times = get_commit_time(file_path)#対象ファイルのパス(現在の階層含まないスラッシュなし)
            print(times)
            i=0
            for commits_hash in hashes:
                
                content = get_content_file_at_commit (commits_hash, file_path)#現在の階層含まない(スラッシュ含まない)
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
                delete_path = Path(f"/Users/yamadanaruto/Desktop/mothertests/{times[i]}")
                if delete_path.exists():
                    shutil.rmtree(delete_path)
                    print("フォルダごと削除しました")
                    i+=1
        #pynose_output2を名前を変えてcollect_jsonに複製
        result = subprocess.run(
                    ['cp','-r', '/Users/yamadanaruto/Desktop/pynose_output2', f'/Users/yamadanaruto/Desktop/collect_json/{filename}'],
                            capture_output=True,
                            text=True,
                            check=True
                    )
        #pynose_outout2のフォルダの中身をカラにする    
        delete_path = Path("/Users/yamadanaruto/Desktop/pynose_output2")  
        for item in delete_path.iterdir():
            if item.is_dir():
                shutil.rmtree(item)
            else:
                item.unlink()      
if __name__ == "__main__":
    main()

    


                         

        
            