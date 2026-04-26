import csv
from datetime import datetime
from pathlib import Path
import pandas as pd
data1 = """date,test_file_count,test_case_count,test_method_count,AssertionRoulette,ConditionalTestLogic,ConstructorInitialization,DefaultTest,DuplicateAssertion,EmptyTest,ExceptionHandling,GeneralFixture,IgnoredTest,LackCohesion,MagicNumberTest,ObscureInLineSetup,RedundantAssertion,RedundantPrint,SleepyTest,SuboptimalAssert,TestMaverick,UnknownTest,total
2025-12-04 02:59:14,1,1,2,1,1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,3
2025-11-14 19:04:38,1,1,2,1,1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,3
2025-11-08 21:07:50,1,1,2,1,1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,3
2025-11-09 15:56:21,1,1,2,1,1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,3
2025-11-09 14:18:55,1,1,2,1,1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,3
"""
data2 ="""date,maintainability
2020-08-19 00:11:35,8
2021-03-21 21:10:57,8
2022-04-22 18:16:32,8
2022-04-27 21:41:42,8
2023-01-21 09:04:31,8
2023-10-31 13:49:36,8
2023-10-31 14:59:07,8
2024-09-05 09:11:03,9
2024-10-20 15:21:04,9
2024-10-20 21:46:35,9
2025-03-24 16:33:03,8
2025-04-26 00:06:46,8
2025-11-09 01:22:33,8
2025-11-09 13:03:45,8
2025-11-09 14:16:32,8
2025-11-09 14:18:55,8
2025-11-09 14:29:30,8
2025-11-09 18:20:46,8
2025-11-12 15:52:32,8
2025-11-12 17:53:46,8
2025-11-12 20:27:58,8
2025-11-12 20:52:12,8
2025-11-13 10:44:36,8
2025-11-15 02:04:38,8
2025-11-16 23:29:52,8
2025-11-21 15:23:18,8
2025-11-26 00:24:54,8
2025-11-26 23:29:42,8
2025-11-28 12:02:42,23
2025-11-28 13:20:44,23
2025-11-29 10:04:22,23
2025-12-04 13:00:08,23
2025-12-05 17:06:19,23
2025-12-06 13:37:11,23
2025-12-06 16:56:14,23
2025-12-06 18:32:13,23
2025-12-06 21:08:50,23
2025-12-06 22:15:19,23
2025-12-06 22:24:12,23
2025-12-07 01:52:28,23
2025-12-07 21:33:01,23
2025-12-11 12:21:55,23
2025-12-17 11:20:30,23
2025-12-18 00:45:59,23
2025-12-19 00:09:52,23
2025-12-24 20:46:50,23"""
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


def main():
    result_Tsmells = sort_date(data1)
    result_Csmells = sort_date(data2)

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
            i += 1
        else:
            date = result_Csmells[t]['date']
            latest_codesmells = result_Csmells[t]['maintainability']
            t += 1

        if latest_total is None or latest_codesmells is None:
            continue

        line = [date, latest_total, latest_codesmells]
        result_line.append(line)

    print(result_line)
    aggregated_df = pd.DataFrame(result_line, columns=['date', 'testsmells', 'codesmells'])
    output_path = Path(__file__).with_name('aggregated.csv')
    aggregated_df.to_csv(output_path, index=False)
    print('Aggregated result generated')


if __name__ == "__main__":
    main()
