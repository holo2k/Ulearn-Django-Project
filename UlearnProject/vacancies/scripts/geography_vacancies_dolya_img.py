import os
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt


def create_pie(df, title, img_path):
    # Создание круговой диаграммы
    df = df.head(20)
    fig, ax = plt.subplots()
    wedges, texts, autotexts = ax.pie(df['Доля вакансий в %'], labels=None, startangle=90, autopct='',
                                      pctdistance=0.85)
    ax.axis('equal')
    ax.set_title(title)

    # Создание легенды с названиями городов
    legend_labels = df['Город']
    ax.legend(legend_labels, loc='center left',
              bbox_to_anchor=(1, 0.5), title='Города')

    # Скрытие текстовых меток на круговой диаграмме
    for text in texts + autotexts:
        text.set_visible(False)

    # Сохранение диаграммы
    fig.savefig(img_path, bbox_inches='tight')
    plt.close(fig)
    print(f"Saved {os.path.basename(img_path)}")


def run():
    # Подключение к базе данных
    conn = sqlite3.connect('db.sqlite3')  # Используйте имя вашей базы данных

    # Выполнение первого SQL-запроса (все вакансии)
    query_all = """
        SELECT
            area_name AS 'Город',
            ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM vacancies), 2) AS 'Доля вакансий в %'
        FROM vacancies
        GROUP BY area_name
        ORDER BY COUNT(*) DESC
    """

    df_all = pd.read_sql_query(query_all, conn)

    query_sharp = """
        SELECT
            area_name AS 'Город',
            ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM vacancies), 3) AS 'Доля вакансий в %'
        FROM vacancies
        WHERE name LIKE '%c#%'
            OR name LIKE '%c sharp%'
            OR name LIKE '%шарп%'
            OR name LIKE '%C#%'
        GROUP BY area_name
        ORDER BY COUNT(*) DESC
    """

    df_sharp = pd.read_sql_query(query_sharp, conn)

    output_dir_html = 'tables'

    output_html_path_all = os.path.join(
        output_dir_html, f'vacancies_pie_all.html')
    output_html_path_sharp = os.path.join(
        output_dir_html, f'vacancies_pie_sharp.html')

    # Закрытие соединения с базой данных
    conn.close()

    # Создание круговой диаграммы для всех вакансий
    create_pie(df_all, 'Доля вакансий по городам (все вакансии)',
               os.path.join('images', 'geography_pie_all.png'))

    # Создание круговой диаграммы для вакансий бэка
    create_pie(df_sharp, 'Доля вакансий C# программиста по городам',
               os.path.join('images', 'geography_pie_sharp.png'))

    df_sharp = df_sharp.reset_index()
    df_sharp.to_html(output_html_path_sharp, index=False, justify='center')

    df_all = df_all.reset_index()
    df_all.to_html(output_html_path_all, index=False, justify='center')


run()
