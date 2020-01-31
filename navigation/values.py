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
    def has_secondary(self):
        has_secondary_highlight = False
        for item in self.get('columns'):
            if item.block_type == 'secondary_highlight':
                has_secondary_highlight = True
        return has_secondary_highlight

    def num_columns(self):
        return len(self.get('columns'))

    def num_columns_max(self):
        max_num = 4
        num_cols = len(self.get('columns'))
        if num_cols > max_num:
            return ceil(num_cols / 2)
        return num_cols

    def num_rows(self):
        if self.has_secondary() and len(self.get('columns')) > 3:
            return 2
        return 1

    def num_columns_row_1(self):
        has_secondary = self.has_secondary()
        num_cols = self.num_columns()
        if has_secondary and num_cols <= 3:
            return num_cols - 1
        else:
            return num_cols

    def num_columns_row_2(self):
        has_secondary = self.has_secondary()
        num_cols = self.num_columns()
        if has_secondary:
            return ceil(num_cols / 2) - 1
        else:
            return ceil(num_cols / 2)

    def column_container_class_row_1(self):
        return 'l-%sup' % str(self.num_columns_row_1())

    def column_container_class_row_2(self):
        return 'l-%sup' % str(self.num_columns_row_2())

    def column_class_row_1(self):
        return 'l-%sup__col' % str(self.num_columns_row_1())

    def column_class_row_2(self):
        return 'l-%sup__col' % str(self.num_columns_row_2())


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
