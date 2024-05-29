from django.core.management.base import BaseCommand
#from .tasks import export_data_to_s3
from ...tasks import export_data_to_s3

class Command(BaseCommand):
    help = 'Export user data to S3'


    def handle(self, *args, **kwargs):
        export_data_to_s3.delay()

