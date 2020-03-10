import requests
import time
import re
from bs4 import BeautifulSoup


def get_briefs_urls():
    base_url = 'https://www.americanbar.org/groups/committees/amicus/1998-present/'
    url_prefix = 'https://www.americanbar.org/'
    page = requests.get(base_url)
    soup = BeautifulSoup(page.content, 'html5lib')


    content_download_regex = re.compile('/content/dam/aba/administrative/amicus/', re.IGNORECASE)
    urls = []
    for row in soup.findAll('a', attrs={'href': content_download_regex}):
        print(row)
        urls.append({
            'title': row.text,
            'url': url_prefix + row.get('href') if not row.get('href').startswith(url_prefix) else row.get('href')
        })
    return urls



def download_files(urls):
    BASE_PATH = '/Users/bradwindsor/programming/research-projects/fed_notes/downloads/amicus-briefs/{}.{}'
    failed = []
    for mins in urls:
        time.sleep(3)
        try:
            response = requests.get(mins['url'])
            ext = 'pdf'
            file_name = BASE_PATH.format(re.sub(r'^[W+]', '_', mins['title']).replace(' ', '_'), ext)
            with open(file_name, 'wb') as f:
                f.write(response.content)
        except Exception as e:
            print('failed', mins['url'])
            failed.append(mins)
    print(len(urls) - len(failed), 'files processed')
    print('failed:', failed)


download_urls = get_briefs_urls()
download_files(download_urls)