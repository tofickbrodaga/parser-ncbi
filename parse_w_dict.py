import os
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

def download_ncbi_images(article_id, save_dir):
    url = f'https://www.ncbi.nlm.nih.gov/pmc/articles/{article_id}/'
    ua = UserAgent()
    headers = {'User-Agent': ua.chrome}

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    figures = soup.find_all('div', class_='fig iconblock whole_rhythm')
    
    if not figures:
        print(f'No figures found on the page for article ID {article_id}.')
        return
    
    captions_dict = {}
    
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    
    for figure in figures:
        img_tag = figure.find('img')
        if img_tag and 'src' in img_tag.attrs:
            img_url = img_tag['src']
            if not img_url.startswith('http'):
                img_url = f'https://www.ncbi.nlm.nih.gov{img_url}'
            img_name = os.path.basename(img_url)
            
            print(f'Image URL: {img_url}')
            print(f'Image Name: {img_name}')
            
            if img_name:
                img_response = requests.get(img_url, headers=headers)
                img_path = os.path.join(save_dir, img_name)
                with open(img_path, 'wb') as img_file:
                    img_file.write(img_response.content)
                
                print(f'Saved image: {img_path}')
            
                caption_tag = figure.find('div', class_='caption')
                if caption_tag:
                    p_tag = caption_tag.find('p')
                    if p_tag:
                        captions_dict[img_name] = p_tag.text.strip()
                        print(f'Found caption for {img_name}')
            else:
                print('Warning: Image name is empty, skipping download.')
        else:
            print('No image found in figure.')
    
    captions_file_path = os.path.join(save_dir, 'captions.txt')
    with open(captions_file_path, 'w', encoding='utf-8') as caption_file:
        for img_name, caption in captions_dict.items():
            caption_file.write(f'{img_name}: {caption}\n')
    
    print(f'Captions saved to {captions_file_path}')
    return captions_dict

def main():
    with open('state.txt', 'r', encoding='utf-8') as file:
        article_ids = file.read().splitlines()
    
    for article_id in article_ids:
        save_dir = os.path.join(os.getcwd(), article_id)
        if os.path.exists(save_dir):
            print(f'Directory for article ID {article_id} already exists. Skipping...')
            continue
        download_ncbi_images(article_id, save_dir)

if __name__ == "__main__":
    main()
