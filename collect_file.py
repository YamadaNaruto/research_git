#コミット数条件を満たすテストファイルを集めるコード
import subprocess
from pathlib import Path

def find_test_file(repo_root):
     return (list(Path(repo_root).rglob("test*.py")))

find_test_file('/Users/yamadanaruto/research_git/public-apis')

def commit_count(file_path):
    result = subprocess.run(
     #コミット数を調べる
        ['git', 'log', '--pretty=format:%H', '--', str(file_path)],
        capture_output=True,
        text=True,
        check=True
    )
    return len(result.stdout.splitlines())
tests = find_test_file('/Users/yamadanaruto/research_git/public-apis')
for test in tests:
     print(commit_count(test),test)