import os
import requests
from fake_useragent import UserAgent
from bs4 import BeautifulSoup

def fetch_article_content(article_id):
    ua = UserAgent()
    headers = {
        'User-Agent': ua.chrome,
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
    }

    url = f'https://www.ncbi.nlm.nih.gov/pmc/articles/{article_id}/'

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        if response.status_code == 403:
            print(f'Access forbidden for article {article_id}: HTTP 403 error')
        elif response.status_code == 500:
            print(f'Internal server error for article {article_id}: HTTP 500 error')
        else:
            print(f'HTTP error for article {article_id}: {e}')
        return None
    except Exception as e:
        print(f'Failed to fetch article {article_id}: {e}')
        return None

    soup = BeautifulSoup(response.content, 'html.parser')

    sections = soup.find_all('div', id=lambda x: x and x.startswith('sec'))

    content = []
    for section in sections:
        section_text = section.get_text(strip=True)
        content.append(section_text)

    return '\n\n'.join(content)

def save_article_content(article_id, content, folder_path):
    file_path = os.path.join(folder_path, f'{article_id}.txt')
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(content)

def main(input_file, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    with open(input_file, 'r') as file:
        article_ids = file.read().splitlines()

    for article_id in article_ids:
        file_path = os.path.join(output_folder, f'{article_id}.txt')
        if os.path.exists(file_path):
            print(f'File for article {article_id} already exists. Skipping...')
            continue

        print(f'Fetching content for article {article_id}...')
        content = fetch_article_content(article_id)
        if content:
            save_article_content(article_id, content, output_folder)
            print(f'Content for article {article_id} saved.')
        else:
            print(f'Failed to fetch content for article {article_id}.')

input_file = 'state.txt'
output_folder = 'articles'

main(input_file, output_folder)
