from tests.dj_rf.models import Publisher

from dj_rql.filter_cls import RQLFilterClass


class PublisherFilters(RQLFilterClass):
    MODEL = Publisher
    SELECT = False
    EXCLUDE_FILTERS = ['authors', 'fk1.publisher', 'fk1.author', 'fk2', 'invalid']
    FILTERS = [
    {
        "filter": "id",
        "ordering": True,
        "search": False
    },
    {
        "filter": "name",
        "ordering": True,
        "search": True
    },
    {
        "namespace": "fk1",
        "filters": [
            {
                "filter": "id",
                "ordering": True,
                "search": False
            }
        ],
        "qs": None
    }
]
