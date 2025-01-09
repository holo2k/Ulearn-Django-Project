# python manage.py runscript demand_vacancy_salary_img -v2

import os
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


def run():
    conn = sqlite3.connect('db.sqlite3')

    query_avg_salary = """
    SELECT
        SUBSTR(published_at, 1, 4) AS 'Год',
        ROUND(AVG(salary), 2) AS 'Средняя з/п'
    FROM vacancies
    WHERE salary IS NOT NULL AND salary < 10000000
    GROUP BY SUBSTR(published_at, 1, 4)
    ORDER BY SUBSTR(published_at, 1, 4)
    """

    df_avg_salary = pd.read_sql_query(query_avg_salary, conn)

    query_avg_salary_sharp = """
    SELECT
        SUBSTR(published_at, 1, 4) AS 'Год',
        ROUND(AVG(salary), 2) AS 'Средняя з/п для C# программиста'
    FROM vacancies
    WHERE 
        salary IS NOT NULL AND salary < 10000000
        AND
        (name LIKE '%c#%'
        OR name LIKE '%C#%'
        OR name LIKE '%c sharp%'
        OR name LIKE '%шарп%'
        OR name LIKE '%С#%')
    GROUP BY SUBSTR(published_at, 1, 4)
    ORDER BY SUBSTR(published_at, 1, 4)
    """

    df_avg_salary_sharp = pd.read_sql_query(query_avg_salary_sharp, conn)

    conn.close()

    fig_avg_salary, ax_avg_salary = plt.subplots()
    ax_avg_salary.plot(
        df_avg_salary['Год'], df_avg_salary['Средняя з/п'], label='Средняя зарплата', marker='o')
    ax_avg_salary.set_title('Средняя зарплата по годам для всех вакансий')
    ax_avg_salary.legend()
    ax_avg_salary.grid(axis='y')

    plt.xticks(rotation=60)

    img_path_avg_salary = os.path.join('images', 'avg_salary.png')
    fig_avg_salary.savefig(img_path_avg_salary)
    plt.close(fig_avg_salary)
    print("Saved")

    fig_avg_salary_sharp, ax_avg_salary_sharp = plt.subplots()
    ax_avg_salary_sharp.plot(df_avg_salary_sharp['Год'], df_avg_salary_sharp['Средняя з/п для C# программиста'],
                             label='Средняя зарплата', marker='o')
    ax_avg_salary_sharp.set_title(
        'Средняя зарплата по годам для C# программиста')
    ax_avg_salary_sharp.legend()
    ax_avg_salary_sharp.grid(axis='y')

    plt.xticks(rotation=60)

    img_path_avg_salary_sharp = os.path.join(
        'images', 'avg_salary_sharp.png')
    fig_avg_salary_sharp.savefig(img_path_avg_salary_sharp)
    plt.close(fig_avg_salary_sharp)

    output_dir_html = 'tables'

    output_html_path_all = os.path.join(
        output_dir_html, f'vacancies_avg_salary_all.html')
    output_html_path_sharp = os.path.join(
        output_dir_html, f'vacancies_avg_salary_sharp.html')
    df_avg_salary = df_avg_salary.head(20)
    df_avg_salary_sharp = df_avg_salary_sharp.head(20)
    df_avg_salary_sharp = df_avg_salary_sharp.reset_index()
    df_avg_salary_sharp.to_html(
        output_html_path_sharp, index=False, justify='center')

    df_avg_salary = df_avg_salary.reset_index()
    df_avg_salary.to_html(output_html_path_all, index=False, justify='center')
    print("Saved")


run()
