from django.core.management.base import BaseCommand, CommandParser
import csv
from project.settings import BASE_DIR 
from movies.models import Movie
from bs4 import BeautifulSoup as bs
import requests

try:
    sourse = requests.get('https://www.imdb.com/chart/top/')
    sourse.raise_for_status()
    pics = {}
    soup = bs(sourse.text, 'html.parser')
    movies = soup.find('tbody', class_='lister-list').find_all('tr') # type: ignore

    for movie in movies:
        url = movie.find('td', class_='posterColumn').a
        src = url.find('img')
        id = str(url)[16:25]
        pics[id] = (max(str(src).split(), key=len)[4:].strip('""'))
   

except Exception as e:
    print('nope')

class Command(BaseCommand):
    help = 'mayonese on a escaletor'

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument('--file', type=str, help='file directory')

    def handle(self, *args, **options):
        file = options['file']

        if file:
            with open(str(BASE_DIR)+"/movies/imdb2000/"+file, encoding='utf-8') as dir:
                tsv_file = csv.reader(dir, delimiter="\t")
                for line in tsv_file:
                    if line[0] in pics.keys():
                        models=Movie(imdb_id=line[0], title_type=line[1], name=line[2], adult=line[4], year=line[5], genre=line[-1], pic=pics[line[0]])
                        models.save()
                    else:
                        models=Movie(imdb_id=line[0], title_type=line[1], name=line[2], adult=line[4], year=line[5], genre=line[-1], pic='https://userstyles.org/style_screenshots/214460_after.jpeg')
                        models.save()
                    
                   