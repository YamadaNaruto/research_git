import csv
from datetime import datetime
from pathlib import Path
import pandas as pd
from sort_with_timeline import merge_codesmells
#data1にcsvを読み取ってテストスメルを辞書型で格納
tsmell_folderpath="/Users/yamadanaruto/research_git/aggregated.csv"
df = pd.read_csv(tsmell_folderpath)
data1 = df.to_dict("records")

"codesmellを入手"
data2 =merge_codesmells("/Users/yamadanaruto/research_git/src/add_code_csv")

#dataを日付でソートする
def sort_date(data):



    #時系列ソート
    rows_sorted = sorted(
        data,
        key=lambda x: datetime.strptime(x['date'], "%Y-%m-%d %H:%M:%S")
    )
    result = []
    "totalかmaintainblityか"
    for row in rows_sorted:
        new_row = {
            'date': row['date']
        }
      
        new_row['total'] = row.get('total')
        result.append(new_row)    
    return result  


def main():
    result_Tsmells = sort_date(data1)
    print(result_Tsmells)
    result_Csmells = data2

    i = 0
    t = 0
    result_line = []
    latest_total = None
    latest_codesmells = None
    
    while i < len(result_Tsmells) or t < len(result_Csmells):
        next_tsmell_date = None
        next_csmell_date = None

        if i < len(result_Tsmells):
            next_tsmell_date = datetime.strptime(
                result_Tsmells[i]['date'], "%Y-%m-%d %H:%M:%S"
            )
        if t < len(result_Csmells):
            next_csmell_date = datetime.strptime(
                result_Csmells[t]['date'], "%Y-%m-%d %H:%M:%S"
            )

        if next_csmell_date is None or (
            next_tsmell_date is not None and next_tsmell_date <= next_csmell_date
        ):
            date = result_Tsmells[i]['date']
            latest_total = result_Tsmells[i]['total']
            latest_codesmells = result_Csmells[t-1]['code_smells']
            i += 1
        else:
            date = result_Csmells[t]['date']
            latest_codesmells = result_Csmells[t]['code_smells']
            latest_total = result_Tsmells[i-1]['total']
            t += 1

        if latest_total is None or latest_codesmells is None:
            continue

        line = [date, latest_total, latest_codesmells]
        result_line.append(line)

    print(result_line)
    aggregated_df = pd.DataFrame(result_line, columns=['date', 'testsmells', 'codesmells'])
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    output_path = Path("/Users/yamadanaruto/Desktop/resultofCSV")/f'{timestamp}.csv'
    aggregated_df.to_csv(output_path, index=False)
    print('Aggregated result generated')


if __name__ == "__main__":
    main()
