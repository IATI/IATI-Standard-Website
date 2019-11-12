from pydoc import locate

from django.conf import settings
from django.core.management.base import BaseCommand


class Command(BaseCommand):

    def __init__(self):
        super(Command, self).__init__()
        self.indexes = []
        connections = settings.ES_CONNECTIONS
        indexes = settings.ES_INDEXES
        for name, value in connections.items():
            for index_name, index_class in indexes.get(name):
                self.indexes.append({
                    'connection_name': name,
                    'connection': value,
                    'index_name': index_name,
                    'index_class': index_class,
                })

    def add_arguments(self, parser):
        parser.add_argument(
            '-b', '--batch-size', dest='batch_size', type=int,
            help='Number of items to index at once.'
        )
        parser.add_argument(
            '-r', '--remove', action='store_true', default=False,
            help='Remove objects from the index that are no longer present in \
                  the database.'
        )
        parser.add_argument(
            '-i', '--index', dest='index', type=str,
            help='Specify which index to update.'
        )
        parser.add_argument(
            '-c', '--clear_index', action='store_true', default=False,
            help='Clear and rebuild index.'
        )
        parser.add_argument(
            '-a', '--age', dest='age', default=0,
            help='Number of hours back to consider objects new.'
        )

    def handle(self, *args, **options):

        index = options.get('index')
        clear_index = options.get('clear_index')

        self.batch_size = options.get('batch_size')
        self.remove = options.get('remove')
        self.age = options.get('age')

        indexes = self.get_indexes(index)

        for index in indexes:
            if clear_index:
                self.clear_index(index)
            self.index_documents(index)

    def get_indexes(self, index):
        indexes = self.indexes
        if index:
            indexes = filter(
                lambda x: x['index_name'] == index,
                indexes
            )
        return indexes

    def clear_index(self, index):
        IndexClass = locate(index['index_class'])
        index_obj = IndexClass()
        index_obj.clear_index()

    def index_documents(self, index):
        IndexClass = locate(index['index_class'])
        IndexClass.index_documents(
            index, self.batch_size, self.remove, self.age)
