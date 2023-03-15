from django.core.management.base import BaseCommand, CommandParser
import csv
from project.settings import BASE_DIR 
from movies.models import Person

class Command(BaseCommand):
    help = 'mayonese on a escaletor'

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument('--file', type=str, help='file directory')

    def handle(self, *args, **options):
        file = options['file']

        if file:
            with open(str(BASE_DIR)+"\\movies\\mdb\\"+file, encoding='utf-8') as dir:
                tsv_file = csv.reader(dir, delimiter="\t")
                for line in tsv_file:
                    models=Person(imdb_id=line[0], name=line[1], birthday=line[2], deathday=line[3])
                    models.save()