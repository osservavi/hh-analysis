from config import RAW_DATA_DIR, PROCESSED_DATA_DIR
import pandas as pd
from pathlib import Path
from datetime import datetime

def upload_data():
    df_list = list()
    csv_files = list(RAW_DATA_DIR.glob('vacancies_info_*.csv'))

    if not csv_files:
        raise FileNotFoundError(f"No CSV files found in {RAW_DATA_DIR}")
    
    for file in csv_files:
        try:
            df = pd.read_csv(file)
            df_list.append(df)
        
        except Exception as e:
            print(f"Ошибка при загрузке {file.name}: {e}")   
    
    bulid_df = pd.concat(df_list, ignore_index=True)

    output_file = PROCESSED_DATA_DIR / 'processed_data.csv' # TO DO: check if right
    bulid_df.to_csv(output_file, index=False, encoding='utf-8')
    

def main():
    print(upload_data())

if __name__ == '__main__':
    main()