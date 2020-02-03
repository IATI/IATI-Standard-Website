from math import ceil
from wagtail.core.blocks import StructValue
from navigation.utils import get_localised_field_value


class ModuleStructValue(StructValue):
    def num_columns(self):
        return max(3, len(self.get('columns')))

    def column_container_class(self):
        return 'l-%sup' % str(self.num_columns())

    def column_class(self):
        return 'l-%sup__col' % str(self.num_columns())


class ModuleDoubleStructValue(StructValue):
    def highlight_class(self):
        highlight_class = ''
        if len(self.get('columns')) > 2:
            highlight_class = 'navigation-megamenu__col--small'

        return highlight_class

    def has_secondary(self):
        has_secondary_highlight = False
        for item in self.get('columns'):
            if item.block_type == 'secondary_highlight':
                has_secondary_highlight = True

        return has_secondary_highlight

    def num_columns(self):
        return max(3, len(self.get('columns')))

    def num_columns_max(self):
        max_num = 4
        num_cols = self.num_columns()
        if num_cols > max_num:
            num_cols = ceil(num_cols / 2)
        return num_cols

    def num_rows(self):
        num_rows = 1
        if self.has_secondary() and self.num_columns() > 3:
            num_rows = 2
        return num_rows

    def num_columns_row(self):
        has_secondary = self.has_secondary()
        num_cols = self.num_columns()

        if has_secondary:
            if num_cols < 4:
                num_cols = num_cols + 1
            else:
                num_cols = num_cols - 1

        num_cols = min(num_cols, 4)

        return num_cols

    def column_container_class(self):
        print('l-%sup' % str(self.num_columns_row()))
        return 'l-%sup' % str(self.num_columns_row())

    def column_class(self):
        print('l-%sup__col' % str(self.num_columns_row()))
        return 'l-%sup__col' % str(self.num_columns_row())


class TransStructValue(StructValue):
    def description(self):
        return get_localised_field_value(
            self,
            'description',
            use_get=True,
        )

    def title(self):
        return get_localised_field_value(
            self,
            'title',
            use_get=True,
        )

    def link_label(self):
        return get_localised_field_value(
            self,
            'link_label',
            use_get=True,
        )
