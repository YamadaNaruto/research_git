#フォルダを指定して、その中のcsvファイルを呼び出して値を取り出し、時系列順にソートしていく
import os
import pandas as pd
from datetime import datetime
import shutil
from pathlib import Path
DATE_FMT = "%Y-%m-%d %H:%M:%S"


def sort_date(data):
    rows_sorted = sorted(
        data,
        key=lambda x: datetime.strptime(x['date'][:19], DATE_FMT)
    )
    result = []
    for row in rows_sorted:
        result.append({'date': row['date'], 'total': row.get('total')})
    return result
detect_foldr="/Users/yamadanaruto/research_git/add_code_csv"

def parse_date(s):
    return datetime.strptime(s[:19], DATE_FMT)

def merge_codesmells(folder=detect_foldr):
    
    merged = []
    first = True
    for filename in sorted(f for f in os.listdir(folder) if f.endswith(".csv")):
        filepath = os.path.join(folder, filename)
        df = pd.read_csv(filepath)
        rows = list(df.to_dict("records"))  
        rows = sort_date(rows)
        print(filename)
       
        if first:
            merged = rows
            first = False
            continue

        data1 = merged
        data2 = rows
        merged = []
        i, t = 0, 0
        last_d1, last_d2 = 0, 0

        while i < len(data1) and t < len(data2):
            d1 = parse_date(data1[i]["date"])
            d2 = parse_date(data2[t]["date"])
            if  d1 == d2:
                last_d1 = data1[i]["code_smells"]
                last_d2 = data2[t]["code_smells"]
                date_str = data1[i]["date"] 
                merged.append({"date": date_str, "code_smells": last_d1 + last_d2})
                i += 1
                t += 1
            elif d1 < d2:
                last_d1 = data1[i]["code_smells"]
                merged.append({"date": data1[i]["date"], "code_smells": last_d1 + last_d2})
                i += 1
            else:
                last_d2 = data2[t]["code_smells"]
                merged.append({"date": data2[t]["date"], "code_smells": last_d1 + last_d2})
                t += 1

        while i < len(data1):
            last_d1 = data1[i]["code_smells"]
            merged.append({"date": data1[i]["date"], "code_smells": last_d1 + last_d2})
            i += 1
        while t < len(data2):
            last_d2 = data2[t]["code_smells"]
            merged.append({"date": data2[t]["date"], "code_smells": last_d1 + last_d2})
            t += 1
              
    return merged

def merge_testsmells(folder):
    merged = []
    first = True
    for filename in sorted(f for f in os.listdir(folder) if f.endswith(".csv")):
        filepath = os.path.join(folder, filename)
        df = pd.read_csv(filepath)
        rows = list(df.to_dict("records"))
        rows = sort_date(rows)  
        print(filename)
        
        if first:
            merged = rows
            first = False
            continue

        data1 = merged
        data2 = rows
        merged = []
        i, t = 0, 0
        last_d1, last_d2 = 0, 0

        while i < len(data1) and t < len(data2):
            d1 = parse_date(data1[i]["date"])
            d2 = parse_date(data2[t]["date"])
            if  d1 == d2:
                last_d1 = data1[i]["total"]
                last_d2 = data2[t]["total"]
                date_str = data1[i]["date"] 
                merged.append({"date": date_str, "total": last_d1 + last_d2})
                i += 1
                t += 1
            elif d1 < d2:
                last_d1 = data1[i]["total"]
                merged.append({"date": data1[i]["date"], "total": last_d1 + last_d2})
                i += 1
            else:
                last_d2 = data2[t]["total"]
                merged.append({"date": data2[t]["date"], "total": last_d1 + last_d2})
                t += 1

        while i < len(data1):
            last_d1 = data1[i]["total"]
            merged.append({"date": data1[i]["date"], "total": last_d1 + last_d2})
            i += 1
        while t < len(data2):
            last_d2 = data2[t]["total"]
            merged.append({"date": data2[t]["date"], "total": last_d1 + last_d2})
            t += 1
         
    print(merged)      
    return merged


        

   


        