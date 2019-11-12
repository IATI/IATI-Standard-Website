import elasticsearch_dsl as es

from . import abstract_index
from home.models import AbstractBasePage

class ArticleBase(abstract_index.DocumentBase):

    heading = es.Text(analyzer='snowball', fields={'raw': es.Keyword()})
    excerpt = es.Text(analyzer='snowball')
    published_from = es.Date()

    class Index:
        name = 'basepage'
        settings = {
            "number_of_shards": 2,
        }

    def get_model(self):
        return AbstractBasePage

    def get_index_queryset(self):
        # method overriden from ABC
        return self.get_model().objects.filter(
            state='PUBLISHED'
        )

    def get_updated_field(self):
        return 'published_from'

    def create_document_dict(self, obj):
        # this method is required.
        self.obj = obj

        doc = ArticleBase(
            heading=obj.title,
            excerpt=obj.body,
        )
        doc.meta.id = obj.id
        return doc.to_dict(include_meta=True)
