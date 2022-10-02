from django.core.management import BaseCommand

from bidder.visualize.factory import VisualizeServiceFactory


class Command(BaseCommand):

    def handle(self, *args, **options):
        VisualizeServiceFactory.create().create_line_graph()
