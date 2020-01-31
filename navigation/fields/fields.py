from wagtail.core.fields import StreamField
from wagtail.core.blocks import (
    StreamBlock,
)
from navigation.fields import (
    TypeA,
    TypeB,
    TypeC,
    TypeD,
)


def navigation(blank=False):
    required = not blank
    return StreamField(
        StreamBlock(
            [
                ('type_a', TypeA()),
                ('type_b', TypeB()),
                ('type_c', TypeC()),
                ('type_d', TypeD()),
            ],
            max_num=1,
            required=required,
        ),
        blank=blank
    )
