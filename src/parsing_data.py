import requests
from bs4 import BeautifulSoup
import time
import pandas as pd
from datetime import datetime
import os

def get_vacancy_links(query='Аналитик данных', pages=1):
    '''
    Формирует список ссылок на вакансии в результате поиска на HH.ru
    '''
    base_url = 'https://hh.ru'
    vacancies_list = list()
    headers = {'User-Agent': 
           'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36'}
    
    for page in range(pages):
        url = f'{base_url}/search/vacancy?text={query}&experience=noExperience&page={page}'
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')

        vacancy_cards = soup.find_all('a', {'data-qa': 'serp-item__title'})
        for card in vacancy_cards:
            link = card['href']
            clean_link = link.split('?')[0]
            vacancies_list.append(clean_link)
        
        time.sleep(3)
    
    return vacancies_list

def parse_vacancy_page(url):
    '''
    Собирает данные с каждой вакансии из собранного списка get_vacancy_links()
    '''
    headers = {'User-Agent': 
           'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36'}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    skills = list()
    skills_info = soup.find('li', {'data_qa': 'skills_element'})
    if skills_info:
        skills = [skill.text.strip() for skill in skills_info.find_all('div', class_=lambda x: x and 'label' in x)]

    vacancy_data = {
        'skills': skills
    }

    return vacancy_data

def main():
    '''
    Производит сбор данных и сохраняет их в формате .CSV
    '''
    print('Производится сбор ссылок...')
    links = get_vacancy_links()

    os.makedirs('data/raw', exist_ok=True)

    vacancies_data = list()
    for i, link in enumerate(links):
        print(f'Парсинг {i}й вакансии из {len(links)}: {link}')
        try:
            data = parse_vacancy_page(link)
            vacancies_data.append(data)
        except Exception as e:
            print(f'! Ошибка при парсинге {link}: {e}')
        
        time.sleep(2)

    current_date = datetime.now().strftime("%Y-%m-%d")
    raw_data_filename = f'vacancies_info_{current_date}.csv'
    raw_data_path = os.path.join('data', 'raw', raw_data_filename)
    
    df = pd.DataFrame(vacancies_data)
    df.to_csv(raw_data_path, index=False, encoding='utf-8-sig')
    print(f"Данные сохранены в: {raw_data_path}")


if __name__ == '__main__':
    main()
