import os
from django.conf import settings
import pandas as pd
import matplotlib.pyplot as plt


def run():
    # Создание DataFrame из данных
    df = pd.read_csv('all_skills.csv')

    # Создаем папку для хранения изображений, если она еще не существует
    output_dir = 'images/all_skills/top_skills_by_year'
    os.makedirs(output_dir, exist_ok=True)

    # Перебор уникальных годов
    for year in df['Year'].unique():
        # Фильтрация данных для текущего года
        year_data = df[df['Year'] == year]

        # Группировка по навыкам и суммирование
        skill_counts = year_data.groupby('Skill')['Count'].sum()

        # Сортировка навыков по количеству упоминаний и выбор топ-20
        top_skills = skill_counts.nlargest(20)

        # Построение графика
        plt.figure(figsize=(12, 8))
        top_skills.plot(kind='bar', color='skyblue', edgecolor='black')

        # Настройка отображения
        plt.title(f'Топ-20 навыков {year} года', fontsize=14)
        plt.xlabel('Навык', fontsize=12)
        plt.ylabel('Количество упоминаний', fontsize=12)
        plt.xticks(rotation=45, ha='right', fontsize=10)
        plt.tight_layout()

        # Сохранение графика как изображение
        output_path = os.path.join(output_dir, f'top_skills_{year}.png')
        plt.savefig(output_path)

        # Закрытие графика для экономии памяти
        plt.close()
run()