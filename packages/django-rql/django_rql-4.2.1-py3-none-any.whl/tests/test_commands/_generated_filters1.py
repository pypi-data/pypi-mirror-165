from tests.dj_rf.models import AutoMain

from dj_rql.filter_cls import RQLFilterClass
from dj_rql.qs import NPR, NSR


class AutoMainFilters(RQLFilterClass):
    MODEL = AutoMain
    SELECT = True
    EXCLUDE_FILTERS = []
    FILTERS = [
    {
        "namespace": "parent",
        "filters": [
            {
                "filter": "id",
                "ordering": True,
                "search": False
            },
            {
                "filter": "common_int",
                "ordering": True,
                "search": False
            },
            {
                "filter": "common_str",
                "ordering": True,
                "search": True
            }
        ],
        "qs": NPR('parent')
    },
    {
        "namespace": "reverse_OtM",
        "filters": [
            {
                "filter": "id",
                "ordering": True,
                "search": False
            }
        ],
        "qs": NPR('reverse_OtM')
    },
    {
        "namespace": "reverse_OtO",
        "filters": [
            {
                "filter": "id",
                "ordering": True,
                "search": False
            }
        ],
        "qs": NSR('reverse_OtO')
    },
    {
        "namespace": "reverse_MtM",
        "filters": [
            {
                "filter": "id",
                "ordering": True,
                "search": False
            }
        ],
        "qs": None
    },
    {
        "namespace": "through",
        "filters": [],
        "qs": NPR('through')
    },
    {
        "filter": "id",
        "ordering": True,
        "search": False
    },
    {
        "filter": "common_int",
        "ordering": True,
        "search": False
    },
    {
        "filter": "common_str",
        "ordering": True,
        "search": True
    },
    {
        "namespace": "self",
        "filters": [
            {
                "filter": "id",
                "ordering": True,
                "search": False
            },
            {
                "filter": "common_int",
                "ordering": True,
                "search": False
            },
            {
                "filter": "common_str",
                "ordering": True,
                "search": True
            }
        ],
        "qs": NSR('self')
    },
    {
        "namespace": "related1",
        "filters": [
            {
                "filter": "id",
                "ordering": True,
                "search": False
            }
        ],
        "qs": NSR('related1')
    },
    {
        "namespace": "related2",
        "filters": [
            {
                "filter": "id",
                "ordering": True,
                "search": False
            }
        ],
        "qs": NSR('related2')
    },
    {
        "namespace": "one_to_one",
        "filters": [
            {
                "filter": "id",
                "ordering": True,
                "search": False
            }
        ],
        "qs": NSR('one_to_one')
    },
    {
        "namespace": "many_to_many",
        "filters": [
            {
                "filter": "id",
                "ordering": True,
                "search": False
            }
        ],
        "qs": NPR('many_to_many')
    }
]
