import requests
from bs4 import BeautifulSoup
import re
import time

def get_pages():
    url_form = 'https://www.federalreserve.gov/monetarypolicy/fomchistorical{}.htm'
    years = []
    for year in range(1936, 2015):
        years.append(url_form.format(year))
    return years

"""
'https://www.federalreserve.gov/monetarypolicy/files/fomchistmin19620109.pdf'
'https://www.federalreserve.gov/monetarypolicy/files/fomcmoa19890208.pdf'
'https://www.federalreserve.gov/monetarypolicy/files/fomcminutes20140129.pdf'
https://www.federalreserve.gov/fomc/MINUTES/1994/19940204min.htm

"""
fed_prefix = 'https://www.federalreserve.gov'

meeting_mins_formats = [
    r'.*monetarypolicy/files/fomchistmin.*pdf',
    r'.*monetarypolicy/files/fomcmoa.*pdf',
    r'.*monetarypolicy/files/fomcminutes.*pdf'
]


"""
https://www.federalreserve.gov/boarddocs/press/monetary/2005/20050202/default.htm
"""
press_release = [
    'boarddocs/press/monetary.*',
    '/fomc/.*default.htm.*',
    'newsevents/pressreleases/monetary'
]

"""
https://www.federalreserve.gov/monetarypolicy/beigebook/files/fullreport20120111.pdf
"""
beige_book = [
    'beige.*pdf'
]

meeting_mins_regex = re.compile('|'.join(meeting_mins_formats), re.IGNORECASE)
press_release_regex = re.compile('|'.join(press_release), re.IGNORECASE)
beige_regex = re.compile('|'.join(beige_book), re.IGNORECASE)

def get_meeting_minutes_urls():
    # urls = [get_pages()[0]]
    urls = get_pages()
    minutes_found = []
    for url in urls:
        time.sleep(2)
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html5lib')
        title = ''
        for row in soup.findAll('title'):
            title = row.text

        for row in soup.findAll('a', attrs={'href': meeting_mins_regex}):
            minutes_found.append({
                'category': 'minutes',
                'title': title,
                'subtitle': row.text,
                'subsubtitle': row.get('href').split('/')[-1].replace('.pdf', '').replace('.PDF', ''),
                'url': fed_prefix + row.get('href') if not row.get('href').startswith(fed_prefix) else row.get('href')
            })
        for row in soup.findAll('a', attrs={'href': press_release_regex}):
            if 'beigebook' in row.get('href'):
                continue
            minutes_found.append({
                'category': 'press release',
                'title': title,
                'subtitle': row.text,
                'subsubtitle': ' '.join(row.get('href').split('/')[-3:]).replace('.htm', '').replace('.default.htm', ''),
                'url': fed_prefix + row.get('href') if not row.get('href').startswith(fed_prefix) else row.get('href')
            })
        for row in soup.findAll('a', attrs={'href': beige_regex}):
            minutes_found.append({
                'category': 'beige book',
                'title': title,
                'subtitle': row.text,
                'subsubtitle': ' '.join(row.get('href').split('/')[-3:]).replace('.pdf', '').replace('.PDF', ''),
                'url': fed_prefix + row.get('href') if not row.get('href').startswith(fed_prefix) else row.get('href')
            })

    print('minutes found', len(minutes_found))
    return minutes_found



def download_files(meeting_minutes_urls):
    BASE_PATH = '/Users/bradwindsor/programming/research-projects/fed_notes/downloads/beige-book/{}-{}-{}.{}'
    failed = []
    for mins in meeting_minutes_urls:
        time.sleep(0.5)
        try:
            response = requests.get(mins['url'])
            ext = 'pdf' if mins['category'] == 'minutes' or mins['category'] == 'beige book' else 'htm'
            file_name = BASE_PATH.format(mins['title'], mins['subtitle'], mins['subsubtitle'], ext)
            with open(file_name, 'wb') as f:
                f.write(response.content)
        except Exception as e:
            print('failed', mins['url'])
            failed.append(mins)
    print(len(meeting_minutes_urls) - len(failed), 'files processed')
    print(failed)


 minutes_found = get_meeting_minutes_urls()
print(minutes_found)
print(len(minutes_found), 'mins found')
download_files(minutes_found)

