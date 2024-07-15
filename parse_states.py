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

    response = requests.get(url, headers=headers)
    if response.status_code == 403:
        print('Access forbidden: HTTP 403 error')
        return None

    response.raise_for_status()

    soup = BeautifulSoup(response.content, 'html.parser')

    sections = soup.find_all('div', id=lambda x: x and x.startswith('sec'))

    content = {}
    for section in sections:
        section_id = section.get('id')
        section_text = section.get_text(strip=True)
        content[section_id] = section_text

    return content

article_id = 'PMC8367785'
content = fetch_article_content(article_id)

if content:
    for sec_id, sec_text in content.items():
        print(sec_text)
else:
    print('Failed to fetch the article content.')
