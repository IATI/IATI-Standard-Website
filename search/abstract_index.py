import datetime
import time

from django.conf import settings

import elasticsearch_dsl as es
from elasticsearch.helpers import bulk
from elasticsearch_dsl.connections import connections


class DocumentBase(es.Document):

    def get_index_queryset(self):
        """
        Base queryset for indexing the document.
        Can be overriden while implementation.
        """
        return self.get_model().all()

    @classmethod
    def get_index_config(cls):
        """
        Returns the index config on which current actions are performed.
        {
            'connection_name': 'default',
            'connection': {'hosts': http://localhost:9200},
            'index_name': 'blog',
            'index_class': 'some_app.indexes.Article',
        }
        """
        connections = settings.ES_CONNECTIONS
        indexes = settings.ES_INDEXES
        index_name = cls._index._name

        for name, conn in connections.items():
            # gets name and connection value
            # default, {'hosts': 'localhost'}
            for index, value in indexes.get(name):
                # get indexes in that connection by name
                if index == index_name:
                    # return the desired index
                    return {
                        'connection_name': name,
                        'connection': conn,
                        'index_name': index,
                        'index_class': value,
                    }
        return None

    @classmethod
    def clear_index(cls, index=None):
        """
        Clears the index.
        """
        if not index:
            index = cls.get_index_config()
        if not index:
            raise Exception('Index not found!')

        connections.create_connection(
            hosts=index['connection']['hosts']
        )
        try:
            index_instance = es.Index(index['index_name'])
            index_instance.delete()
        except Exception:
            pass
        connections.remove_connection(index['connection_name'])

    @classmethod
    def index_documents(cls, index=None, batch_size=None, remove=False,
                        age=0):
        """
        Main controller method for indexing the documents.
        """
        if not index:
            index = cls.get_index_config()
        if not index:
            raise Exception('Index not found!')

        if not batch_size:
            batch_size = settings.ES_DEFAULT_BATCH_SIZE

        connections.create_connection(
            hosts=index['connection']['hosts']
        )
        # basically runs Article.init().
        cls.prepare_document()

        # base queryset for indexing the docs.
        base_qset = cls().get_index_queryset()

        # get the recent data if age is specified, default == 0
        if int(age) > 0:
            base_qset = cls.get_recently_updated_qset(base_qset, int(age))

        # perform the indexing
        if base_qset:
            cls.perform_index(base_qset, batch_size)

        # remove the stale values.
        if remove:
            cls.remove_stale(base_qset, batch_size)

        connections.remove_connection(index['connection_name'])

    @classmethod
    def get_recently_updated_qset(cls, base_qset, age):
        """
        Gets the recent data related to updated_field
        Always specify the updated_field as a string.
        """
        updated_field = cls().get_updated_field()
        past_date = datetime.datetime.now() - \
            datetime.timedelta(hours=age)
        updated_field = '{}__gte'.format(updated_field)
        filter_kwargs = {updated_field: past_date}
        return base_qset.filter(**filter_kwargs)

    @classmethod
    def perform_index(cls, base_qset, batch_size):
        """
        Performs the indexing.
        - Gets the queryset slice
        - creates the batch
        - indexes it
        """
        for start in range(0, base_qset.count(), batch_size):
            end = start + batch_size
            qset = base_qset[start:end]
            batch = cls.create_batch(list(qset))
            cls.index_batch(batch)
            time.sleep(0.5)

    @classmethod
    def create_batch(cls, objects):
        """
        Creates the document dict for indexing.
        Uses create_document_dict() method that we defined in our indexes.py
        """
        batch = []
        for obj in objects:
            batch.append(cls().create_document_dict(obj))
        return batch

    @classmethod
    def index_batch(cls, batch):
        """
        Index the specified batch.
        Always index in bulk as it saves resources.
        We have used elasticsearch-py's bulk method here.
        """
        es = connections.get_connection()
        bulk(client=es, actions=batch)

    @classmethod
    def prepare_document(cls):
        """
        refer document lifecylcle
        """
        try:
            cls.init()
        except Exception:
            pass

    @classmethod
    def remove_stale(cls, base_qset, batch_size):
        """
        Removes docuemts that are present in the index but not in the db.
        Index meta id and db instance pk needs to be same.
        """
        db_ids = list(base_qset.values_list('id', flat=True))
        s = cls.search()
        resp = s.execute()
        total_index = resp.hits.total
        removed = []
        for start in range(0, total_index, batch_size):
            end = start + batch_size
            items = resp.hits[start:end]
            for item in items:
                if int(item.meta.id) not in db_ids:
                    removed.append(int(item.meta.id))
        for remove_id in removed:
            cls.get(id=remove_id).delete()
