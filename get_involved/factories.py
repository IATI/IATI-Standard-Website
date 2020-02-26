from get_involved.models import GetInvolvedPage
from home.factories import BasePageFactory


class GetInvolvedPageFactory(BasePageFactory):
    """Factory generating data for GetInvolvedPage."""

    class Meta:
        model = GetInvolvedPage
        django_get_or_create = ('title', 'path',)
