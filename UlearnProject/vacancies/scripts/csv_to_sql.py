import pandas as pd
import sqlite3

df_currency = pd.read_csv('./currency.csv', index_col='date')
csv_merged = pd.read_csv('./vacancies_2024.csv')
csv_merged['id'] = range(1, len(csv_merged) + 1)
csv_merged['published_at'] = pd.to_datetime(csv_merged['published_at'])


def convert_salary(row):
    if pd.notna(row['salary_from']) and pd.notna(row['salary_to']):
        salary = (row['salary_from'] + row['salary_to']) / 2
    elif pd.notna(row['salary_from']):
        salary = row['salary_from']
    elif pd.notna(row['salary_to']):
        salary = row['salary_to']
    else:
        return None

    month_year = row['published_at'].strftime('%Y-%m')

    if row['salary_currency'] != 'RUR':
        currency_rate = df_currency.loc[month_year, row['salary_currency']]
        salary_in_rub = salary * currency_rate
    else:
        salary_in_rub = salary

    return salary_in_rub


csv_merged['salary'] = csv_merged.apply(convert_salary, axis=1)

csv_merged['published_at'] = csv_merged['published_at'].apply(
    lambda x: x.strftime("%Y-%m-%dT%H:%M:%S%z") if pd.notna(x) else None)

conn = sqlite3.connect('db.sqlite3')
result_csv = csv_merged[['id', 'name', 'salary', 'area_name', 'published_at']]

result_csv.to_sql('vacancies', con=conn, if_exists='append', index=False)

conn.commit()
conn.close()
