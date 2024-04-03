from flask import Flask, render_template
from sqlalchemy import create_engine
import pandas as pd
import os

app = Flask(__name__)

DRIVER_NAME = 'ODBC Driver 17 for SQL Server'
SERVICE_NAME = '113.160.132.124,1434\\WINCC'
DATABASE_NAME = 'KEPSERVER'

def connection_string ( driver_name, sever_name, database_name):
    conn_string = f"mssql+pyodbc://a_binh:123@{sever_name}/{database_name}?driver={driver_name}"
    return conn_string

engine = create_engine(connection_string(DRIVER_NAME,SERVICE_NAME,DATABASE_NAME))

@app.route('/')
def home():
    try:
        print('Kết nối thành công!')

    except Exception as e:
        print('Lỗi kết nối:')
        print(str(e))
    else:
        table_names = ['DH2-KM00', 'DH2-KM01', 'DH2-KM02', 'DH2-KM03', 'DH2-KM04', 'DH2-KM05', 'DH2-KM06', 'DH2-KM07', 'DH2-KM08', 'DH2-KM09', 'DH2-KM10', 'DH2-KM11', 'DH2-KM12', 'DH2-KM13', 'DH2-KM14', 'DH2-KM15', 'DH2-KM16', 'DH2-KM17', 'DH2-KM18', 'DH2-KM19', 'DH2-KM20', 'DH2-KM21', 'DH2-KM22', 'DH2-KM23', 'DH2-KM24', 'DH2-KM25', 'DH2-KT01', 'DH2-KT02', 'DH2-KT03', 'DH2-KT04', 'DH2-KT05', 'DH2-KT06', 'DH1-KT02']
        all_data = []
        for table_name in table_names:
            sql_query = f'SELECT TOP (1) [Ngay_gio],[Trang_thai_may],[Loi],[Quy_cach],[Toc_do],[Trong_luong],[Chieu_dai],[Runtime]FROM [KEPSERVER].[dbo].[{table_name}] ORDER BY Ngay_gio DESC'
            df = pd.read_sql_query(sql_query, engine)
            df = df.assign(Table_Name=table_name)
            all_data.append(df)
        all_df = pd.concat(all_data, ignore_index=True)
        return all_df.to_html()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000)) # Nếu không tìm thấy biến môi trường 'PORT', sẽ sử dụng 5000 làm mặc định
    app.run(host='0.0.0.0', port=port)
