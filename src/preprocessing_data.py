from config import RAW_DATA_DIR, PROCESSED_DATA_DIR
import pandas as pd
from pathlib import Path
from datetime import datetime

def upload_data():
    df_lst = list()
    csv_files = list(RAW_DATA_DIR.glob('vacancies_info_*.csv'))

    if not csv_files:
        raise FileNotFoundError(f"No CSV files found in {RAW_DATA_DIR}")
    
    for data_file in csv_files:
        try:
            creation_timestamp = data_file.stat().st_birthtime
            creation_date = datetime.fromtimestamp(creation_timestamp)

            df = pd.read_csv(data_file)
            df['collecting_date'] = creation_date
            df_lst.append(df)
        
        except Exception as e:
            print(f"Ошибка при загрузке {data_file.name}: {e}")   
    
    return pd.concat(df_lst, ignore_index=True)

def main():
    print(upload_data())

if __name__ == '__main__':
    main()