#git log からコミットごとにテストスメルを検出してCSVに保存するスクリプト
import subprocess
import os
import shutil
from pathlib import Path
from get_csv_stats2 import get_csv
import sys
import json

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
        ['git','log','--pretty=format:%ad','--date=format:%Y-%m-%d %H:%M:%S','--',file_path],
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
    test_dirs = json.loads(Path(sys.argv[1]).read_text())
    print(test_dirs)
    l = 0
    #フォルダを読み込んでファイルを取得
    for item in test_dirs:
        repo_root = item['repo_root']
        folder_path = item['test_dir']
        os.chdir(repo_root)
        print(folder_path)
        k = 0
        result =subprocess.run(
                ['find', '/Users/yamadanaruto/Desktop', '-name', '.DS_Store', '-delete'],
                capture_output=True,
                text=True,
        )
        if result.returncode != 0:
            print(f"collect_testsmels.py エラー:\n{result.stderr}")    

        for curdir,dirs,files in os.walk(folder_path):#os.walkを使ってフォルダの中まで検出するように
            for filename in files:
                if not (filename.endswith('.py') and (filename.startswith('test_') or filename.endswith('_test.py'))):
                    print("スキップ1")
                    continue
                #print(os.path.join(curdir,filename))
                file_path = os.path.join(curdir, filename)
                print(file_path);    
                hashes = get_hashes_of_file(file_path)#対象ファイルのパス(現在の階層含まないスラッシュなし)
                times = get_commit_time(file_path)#対象ファイルのパス(現在の階層含まないスラッシュなし)
                #print(times)
                i=0
                for commits_hash in hashes:
                    
                    content = get_content_file_at_commit (commits_hash, file_path)
                    #例外をスキップ
                    if content is None:
                        print("中身が空")
                        i+=1
                        continue


                #ファイルに内容を書き込む
                
                    path = Path(f'/Users/yamadanaruto/Desktop/mothertests/{times[i]}/test_{k}.py')
                    path.parent.mkdir(parents=True, exist_ok=True)
                    path.write_text(content)
                    i+=1   
                    k+=1
            #テストスメル検出するコマンドを実行
                try:
                    result = subprocess.run(
                        ['python3', '/Users/yamadanaruto/Desktop/PyNose-ASE2022/runner.py'],
                        capture_output=True,
                        text=True,
                        timeout=600,
                    )
                    if result.returncode != 0:
                        print(f"collect_testsmels.py エラー:\n{result.stderr}")
                except subprocess.TimeoutExpired:
                    print(f"タイムアウトスキップ: {file_path}")
                    shutil.rmtree('/Users/yamadanaruto/Desktop/mothertests', ignore_errors=True)
                    l+=1
                    continue

                get_csv(l)
                l+=1
                shutil.rmtree('/Users/yamadanaruto/Desktop/mothertests', ignore_errors=True)
    result = subprocess.run(
            ['python3', '/Users/yamadanaruto/research_git/src/merge_testsmell_and_codesmell.py'],
            capture_output=True,
            text=True,
            check=True
        )
    if result.returncode != 0:
        print(f"collect_testsmels.py エラー:\n{result.stderr}")



if __name__ == '__main__':
    
    main()


