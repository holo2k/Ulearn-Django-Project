import django
import os
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


def run():
    conn = sqlite3.connect('db.sqlite3')

    query_all = """
    SELECT
        SUBSTR(published_at, 1, 4) AS 'Год',
        COUNT(*) AS 'Количество вакансий'
    FROM vacancies
    GROUP BY SUBSTR(published_at, 1, 4)
    ORDER BY SUBSTR(published_at, 1, 4)
    """

    df_all = pd.read_sql_query(query_all, conn)

    query_sharp = """
    SELECT
        SUBSTR(published_at, 1, 4) AS 'Год',
        COUNT(*) AS 'Количество вакансий для C# программиста'
    FROM vacancies
    WHERE name LIKE '%c#%'
        OR name LIKE '%c sharp%'
        OR name LIKE '%шарп%'
        OR name LIKE '%C#%'
    GROUP BY SUBSTR(published_at, 1, 4)
    ORDER BY SUBSTR(published_at, 1, 4) 
    """

    df_sharp = pd.read_sql_query(query_sharp, conn)

    conn.close()

    fig_all, ax_all = plt.subplots()
    years_all = np.arange(len(df_all['Год']))
    ax_all.bar(
        x=years_all, height=df_all['Количество вакансий'], width=0.4, label='Количество вакансий')
    ax_all.set_title('Количество всех вакансий по годам')
    ax_all.set_xticks(years_all)
    ax_all.set_xticklabels(df_all['Год'], rotation=90, ha='center')
    ax_all.legend()
    ax_all.grid(axis='y')

    img_path_all = os.path.join('images',  'vacancies_all.png')
    fig_all.savefig(img_path_all)
    plt.close(fig_all)
    print("Saved")

    fig_sharp, ax_sharp = plt.subplots()
    years_sharp = np.arange(len(df_sharp['Год']))
    ax_sharp.bar(
        x=years_sharp, height=df_sharp['Количество вакансий для C# программиста'], width=0.4, label='Количество вакансий')
    ax_sharp.set_title(
        'Количество вакансий для C# программиста')
    ax_sharp.set_xticks(years_sharp)
    ax_sharp.set_xticklabels(df_sharp['Год'], rotation=90, ha='center')
    ax_sharp.legend()
    ax_sharp.grid(axis='y')

    img_path_sharp = os.path.join('images', 'vacancies_count_sharp.png')
    fig_sharp.savefig(img_path_sharp)
    plt.close(fig_sharp)

    output_dir_html = 'tables'

    output_html_path_all = os.path.join(
        output_dir_html, f'vacancies_count_all.html')
    output_html_path_sharp = os.path.join(
        output_dir_html, f'vacancies_count_sharp.html')

    df_all = df_all.head(20)
    df_sharp = df_sharp.head(20)
    df_sharp = df_sharp.reset_index()
    df_sharp.to_html(output_html_path_sharp, index=False, justify='center')

    df_all = df_all.reset_index()
    df_all.to_html(output_html_path_all, index=False, justify='center')
    print("Saved")


run()
