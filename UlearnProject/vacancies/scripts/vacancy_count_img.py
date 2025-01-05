import django
import os
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


def run():
    # Подключение к базе данных
    conn = sqlite3.connect('db.sqlite3')  # Используйте имя вашей базы данных

    # Выполнение первого SQL-запроса
    query_all = """
    SELECT
        SUBSTR(published_at, 1, 4) AS 'Год',
        COUNT(*) AS 'Количество вакансий'
    FROM vacancies
    GROUP BY SUBSTR(published_at, 1, 4)
    ORDER BY SUBSTR(published_at, 1, 4)
    """

    df_all = pd.read_sql_query(query_all, conn)

    # Выполнение второго SQL-запроса
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

    # Закрытие соединения с базой данных
    conn.close()

    # Создание графика для всех вакансий
    fig_all, ax_all = plt.subplots()
    years_all = np.arange(len(df_all['Год']))
    ax_all.bar(
        x=years_all, height=df_all['Количество вакансий'], width=0.4, label='Количество вакансий')
    ax_all.set_title('Количество всех вакансий по годам')
    ax_all.set_xticks(years_all)
    ax_all.set_xticklabels(df_all['Год'], rotation=90, ha='center')
    ax_all.legend()
    ax_all.grid(axis='y')

    # Сохранение графика для всех вакансий как изображения
    img_path_all = os.path.join('images',  'vacancies_all.png')
    fig_all.savefig(img_path_all)
    plt.close(fig_all)  # Закрыть график, чтобы освободить ресурсы
    print("Saved")

    # Создание графика для вакансий бэка
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

    # Сохранение графика для вакансий бэка как изображения
    img_path_sharp = os.path.join('images', 'vacancies_count_sharp.png')
    fig_sharp.savefig(img_path_sharp)
    plt.close(fig_sharp)  # Закрыть график, чтобы освободить ресурсы
    print("Saved")


run()
