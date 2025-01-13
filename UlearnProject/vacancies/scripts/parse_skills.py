import csv
from collections import Counter


def save_skills_to_csv(filename, data):
    with open(filename, mode='w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Year', 'Skill', 'Count'])
        for year, skills_count in data.items():
            for skill, count in skills_count.items():
                writer.writerow([year, skill, count])


def run():
    skills_all_by_year = {}
    skills_sharp_by_year = {}

    with open('vacancies_2024.csv', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)

        for row in reader:
            year = row['published_at'][:4]
            skills = row['key_skills'].split('\n')

            skills = [skill.strip() for skill in skills if skill.strip()]

            if year in skills_all_by_year:
                skills_all_by_year[year].extend(skills)
            else:
                skills_all_by_year[year] = skills

            sharp_keywords = ['c#', 'C#', 'c sharp', 'шарп', 'С#']
            if any(word in row['name'].lower() for word in sharp_keywords):
                if year in skills_sharp_by_year:
                    skills_sharp_by_year[year].extend(skills)
                else:
                    skills_sharp_by_year[year] = skills

    for data, filename in zip([skills_all_by_year, skills_sharp_by_year],
                              ['all_skills.csv', 'sharp_skills.csv']):
        with open(filename, mode='w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Year', 'Skill', 'Count'])
            for year, skills in data.items():
                skills_count = Counter(skills)
                for skill, count in skills_count.most_common(20):
                    writer.writerow([year, skill, count])

    print("Done")


run()
