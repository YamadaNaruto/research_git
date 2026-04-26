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
    # git show には repo root からの相対パスが必要
    rel_path = os.path.relpath(file_path)
    try:
        content = subprocess.run(
            ['git', 'show', f'{commit_hash}:{rel_path}'],
            capture_output=True,
            text=True,
            check=True
        ).stdout
    except subprocess.CalledProcessError:
        print(f"スキップ:{commit_hash}に{file_path}が存在しない")
        return None
    return content
       
def main():
    #フォルダを読み込んでファイルを取得
    folder_path = "tests"
    k = 0
    for curdir,dirs,files in os.walk(folder_path):#os.walkを使ってフォルダの中まで検出するように
        for filename in files:
            #.pyじゃなければスキップ
            if not filename.endswith('.py'):
                continue
            #print(os.path.join(curdir,filename))
            file_path = os.path.join(curdir, filename)
            print(file_path);    
            hashes = get_hashes_of_file(file_path)#対象ファイルのパス(現在の階層含まないスラッシュなし)
            times = get_commit_time(file_path)#対象ファイルのパス(現在の階層含まないスラッシュなし)
            print(times)
            i=0
            for commits_hash in hashes:
                
                content = get_content_file_at_commit (commits_hash, file_path)
                #例外をスキップ
                if content is None:
                    continue
                #print(f'Commit: {commits_hash}\nContent:\n{content}\n')    

            #ファイルに内容を書き込む
             
                path = Path(f'/Users/yamadanaruto/Desktop/mothertests/{times[i]}/test_{k}.py')
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(content)
                i+=1   
                k+=1
                
                
                
#テストスメル検出するコマンドを実行
    result = subprocess.run(
                ['python3', '/Users/yamadanaruto/Desktop/PyNose-ASE2022/runner.py'],
                        capture_output=True,
                        text=True,
                        check=True
                )
    delete_path = Path("/Users/yamadanaruto/Desktop/mothertests")
    if delete_path.exists():
        shutil.rmtree(delete_path)
        print("フォルダごと削除しました")
                        
    result = subprocess.run(
                ['python3', '/Users/yamadanaruto/research_git/src/get_csv_stats.py'],
                        capture_output=True,
                        text=True,
                        check=True
                )     
    
if __name__ == "__main__":
    main()

    


                         

        
            