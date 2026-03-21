import csv
from collections import defaultdict
from datetime import datetime
import pandas as pd
data1 = """date,test_file_count,test_case_count,test_method_count,AssertionRoulette,ConditionalTestLogic,ConstructorInitialization,DefaultTest,DuplicateAssertion,EmptyTest,ExceptionHandling,GeneralFixture,IgnoredTest,LackCohesion,MagicNumberTest,ObscureInLineSetup,RedundantAssertion,RedundantPrint,SleepyTest,SuboptimalAssert,TestMaverick,UnknownTest,total
2017-04-27 17:36:44,1,3,14,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,3
2018-07-04 15:39:44,1,3,14,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,3
2018-05-21 16:16:41,1,1,8,0,0,0,0,0,0,1,0,0,1,0,0,0,0,0,0,0,1,3
2019-05-15 18:14:43,1,2,9,0,1,0,0,0,0,1,0,0,1,0,0,0,0,0,0,0,1,4
2018-07-03 16:56:57,1,1,8,0,0,0,0,0,0,1,0,0,1,0,0,0,0,0,0,0,1,3
2019-05-17 16:47:28,1,2,10,0,1,0,0,0,0,1,0,0,1,0,0,0,0,0,0,0,1,4
2019-05-17 16:44:04,1,2,9,0,1,0,0,0,0,1,0,0,1,0,0,0,0,0,0,0,1,4
2018-07-04 15:39:44,1,1,8,0,0,0,0,0,0,1,0,0,1,0,0,0,0,0,0,0,1,3
"""
data2 ="""date,maintainability
2019-02-26 16:29:37,1
2019-03-01 08:56:47,1
2019-04-22 15:17:21,1
2019-04-24 11:46:23,4
2019-07-05 16:57:45,4
2019-11-21 15:08:16,4
2020-05-19 17:54:49,4
2020-08-04 10:09:11,1
2022-08-19 16:03:46,1
2023-01-03 12:45:11,1
2024-07-01 13:20:24,1
2024-07-31 16:03:39,1
2024-09-05 18:06:42,1
2025-02-27 15:48:35,1"""
#dataを日付でソートする
def sort_date(data):

    reader = csv.DictReader(data.splitlines())

    rows = list(reader)


    #時系列ソート
    rows_sorted = sorted(
        rows,
        key=lambda x: datetime.strptime(x['date'], "%Y-%m-%d %H:%M:%S")
    )
    result = []
    "totalかmaintainblityか"
    for row in rows_sorted:
        new_row = {
            'date': row['date']
        }
        if row.get('total') is None:
            new_row['maintainability'] = row.get('maintainability')
        else:
            new_row['total'] = row.get('total')
        result.append(new_row)    
    return result        
#データが有効化無効か判断する
def is_valid_date(s):
    try:
        datetime.strptime(s, "%Y-%m-%d %H:%M:%S")
        return True
    except:
        return False

def main():
    result_Tsmells = sort_date(data1)
    print(result_Tsmells)
    result_Csmells = sort_date(data2)
    print(result_Csmells)
    #Tsmellsの１番目とCsmellsの一番上を比較し小さい方(昔)の方をappendするこの時存在しないデータは前
    #の値を使い、前の値がなければなし。採用された方のデータは次の要素に移る、されなかったものはそのまま
    i = 0
    t = 0
    result_line = []
    while i < len(result_Tsmells) or t < len(result_Csmells):
        if ( i>=len(result_Tsmells)):
            date = result_Csmells[t]['date']
            codesmells = result_Csmells[t]['maintainability']
            t+=1
        elif ( t>=len(result_Csmells)):
            date = result_Tsmells[i]['date']
            total = result_Tsmells[i]['total']
            i+=1   
        #テストスメルの方が新しい時
        elif (result_Tsmells[i]['date'] > result_Csmells[t]['date']):
            if (i==0):
                total = None
            date = result_Csmells[t]['date']
            codesmells = result_Csmells[t]['maintainability']
            t+=1
        elif (result_Tsmells[i]['date'] == result_Csmells[t]['date'] ):
            date = result_Csmells[i]['date']
            total = result_Tsmells[i]['total']
            codesmells = result_Csmells[t]['maintainability']
        else :
            if (t==0):
                codesmells = None
            date = result_Tsmells[i]['date']
            total = result_Tsmells[i]['total']
            i+=1
        line = [date , total , codesmells]
        result_line.append(line)
    print(result_line)
    aggregated_df = pd.DataFrame(result_line, columns=['date','testsmells','codesmells'])    
    aggregated_df.to_csv('/Users/yamadanaruto/Desktop/collect_csv/aggregated.csv', index=False)
    print('Aggregated result generated')


if __name__ == "__main__":
    main()