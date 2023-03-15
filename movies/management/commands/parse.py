from bs4 import BeautifulSoup as bs
import requests

try:
    sourse = requests.get('https://www.imdb.com/chart/top/')
    sourse.raise_for_status()

    soup = bs(sourse.text, 'html.parser')
    movies = soup.find('tbody', class_='lister-list').find_all('tr') # type: ignore

    for movie in movies:
        url = movie.find('td', class_='posterColumn').a
        src = url.find('img')
        id = str(url)[16:25]
        print(max(str(src).split(), key=len)[4:].strip('""'))
        print(id)
except Exception as e:
    print('nope')


