import os
import subprocess
import shutil
from pathlib import Path
def main():
    for name in os.listdir('/Users/yamadanaruto/research_git/detectfolder'):
        if not os.path.isdir(f'/Users/yamadanaruto/research_git/detectfolder/{name}'):
            continue
        folder_path1 = Path("/Users/yamadanaruto/research_git/add_code_csv")
        folder_path2 = Path("/Users/yamadanaruto/research_git/add_test_csv")
        if folder_path2.exists():
             
             shutil.rmtree(folder_path2)
             print("フォルダごと削除しました") 
             Path("/Users/yamadanaruto/research_git/add_test_csv").mkdir()  
        
        if folder_path1.exists():
             
             shutil.rmtree(folder_path1)
             print("フォルダごと削除しました") 
             Path("/Users/yamadanaruto/research_git/add_code_csv").mkdir()
        # test_dirs_path = Path('/Users/yamadanaruto/research_git/test_dirs.json')
        # if test_dirs_path.exists():
        #     test_dirs_path.unlink()
            
   
        print(name)
        result = subprocess.run(
                    ['python3', '/Users/yamadanaruto/research_git/src/collect_codesmells2.py',f'{name}'],
                            capture_output=True,
                            text=True,
                    )
        if result.returncode != 0:
            print(f"エラー ({name}):\n{result.stderr}")
    
        shutil.move(f'/Users/yamadanaruto/research_git/detectfolder/{name}',
                    '/Users/yamadanaruto/research_git/serached_repo')

    print('解析終了')     

if __name__ == "__main__":
    main()    