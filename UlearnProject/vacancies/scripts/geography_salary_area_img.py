import os
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# python manage.py runscript geography_salary_area_img -v2


def create_salary_area_graph(df, title, img_path):
    df = df.head(20)
    fig, ax = plt.subplots()
    cities = np.arange(len(df['Город']))
    ax.barh(y=cities, width=df[title],
            height=0.4, label='Уровень зарплат')
    ax.set_title(title)
    ax.set_yticks(cities)
    ax.set_yticklabels(df['Город'], fontsize=6)
    ax.legend()
    ax.grid(axis='x')

    fig.savefig(img_path, bbox_inches='tight')
    plt.close(fig)
    print(f"Saved {os.path.basename(img_path)}")


def run():
    # Подключение к базе данных
    conn = sqlite3.connect('db.sqlite3')  # Используйте имя вашей базы данных

    # Выполнение первого SQL-запроса
    query_all = """
        SELECT
            area_name AS 'Город',
            ROUND(AVG(salary), 2) AS 'Уровень зарплат по городам'
        FROM vacancies
        WHERE salary < 10000000
        GROUP BY area_name
        ORDER BY ROUND(AVG(salary),2) DESC
    """

    df_all = pd.read_sql_query(query_all, conn)

    # Выполнение второго SQL-запроса
    query_sharp = """
        SELECT
            area_name AS 'Город',
            ROUND(AVG(salary), 2) AS 'Уровень зарплат по городам для C# программиста'
        FROM vacancies
        WHERE name LIKE '%c#%'
            OR name LIKE '%c sharp%'
            OR name LIKE '%шарп%'
            OR name LIKE '%C#%'
            AND salary < 10000000
        GROUP BY area_name
        ORDER BY ROUND(AVG(salary),2) DESC
    """

    df_sharp = pd.read_sql_query(query_sharp, conn)

    output_dir_html = 'tables'

    output_html_path_all = os.path.join(
        output_dir_html, f'salary_area_all.html')
    output_html_path_sharp = os.path.join(
        output_dir_html, f'salary_area_sharp.html')

    # Закрытие соединения с базой данных
    conn.close()

    # Создание графика для всех вакансий
    create_salary_area_graph(df_all, 'Уровень зарплат по городам',
                             os.path.join('images',  'geography_salary_area_all.png'))

    # Создание графика для вакансий бэка
    create_salary_area_graph(df_sharp, 'Уровень зарплат по городам для C# программиста',
                             os.path.join('images',  'geography_salary_area_sharp.png'))
    df_sharp = df_sharp.head(20)
    df_all = df_all.head(20)
    df_sharp = df_sharp.reset_index().rename(columns={
        'Город': 'Город', 'Уровень зарплат по городам для C# программиста': 'Уровень зарплат по городам для C# программиста'})
    df_sharp.to_html(output_html_path_sharp, index=False, justify='center')

    df_all = df_all.reset_index().rename(columns={
        'Город': 'Город', 'Уровень зарплат по городам': 'Уровень зарплат по городам'})
    df_all.to_html(output_html_path_all, index=False, justify='center')


run()
