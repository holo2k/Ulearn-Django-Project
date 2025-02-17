import os
from django.conf import settings
import pandas as pd
import matplotlib.pyplot as plt


def run():
    df = pd.read_csv('all_skills.csv')

    output_dir_images = 'images/all_skills/top_skills_by_year'
    output_dir_html = 'tables/all_skills/top_skills_by_year'
    os.makedirs(output_dir_images, exist_ok=True)
    os.makedirs(output_dir_html, exist_ok=True)

    for year in df['Year'].unique():
        year_data = df[df['Year'] == year]

        skill_counts = year_data.groupby('Skill')['Count'].sum()

        top_skills = skill_counts.nlargest(20)

        plt.figure(figsize=(12, 8))
        top_skills.plot(kind='bar', color='skyblue', edgecolor='black')

        plt.title(f'Топ-20 навыков {year} года', fontsize=14)
        plt.xlabel('Навык', fontsize=12)
        plt.ylabel('Количество упоминаний', fontsize=12)
        plt.xticks(rotation=45, ha='right', fontsize=10)
        plt.tight_layout()

        output_image_path = os.path.join(
            output_dir_images, f'top_skills_{year}.png')
        plt.savefig(output_image_path)

        plt.close()

        output_html_path = os.path.join(
            output_dir_html, f'top_skills_{year}.html')
        top_skills_df = top_skills.reset_index().rename(
            columns={'Skill': 'Навык', 'Count': 'Количество упоминаний'})
        top_skills_df.to_html(output_html_path, index=False, justify='center')

    print(f'Графики сохранены в папке {output_dir_images}')
    print(f'Таблицы сохранены в папке {output_dir_html}')


run()
