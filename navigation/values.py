"""Module to define struct values for navigation."""

from math import ceil
from wagtail.core.blocks import StructValue
from navigation.utils import get_localised_field_value


class ModuleStructValue(StructValue):
    """Mega-navigation struct value."""

    def highlight_class(self):
        """Set highlight class based on width field."""
        return 'navigation-megamenu__col--%s' % self.get('highlight').get('width')

    def num_columns(self):
        """Define number of columns."""
        return max(3, len(self.get('columns')))

    def column_container_class(self):
        """Define column container class."""
        return 'l-%sup' % str(self.num_columns())

    def column_class(self):
        """Define the column class."""
        return 'l-%sup__col' % str(self.num_columns())


class ModuleDoubleStructValue(StructValue):
    """Mega-navigation double struct value."""

    def highlight_class(self):
        """Set highlight class based on width field."""
        return 'navigation-megamenu__col--%s' % self.get('highlight').get('width')

    def has_secondary(self):
        """Define whether navigation has secondary items."""
        has_secondary_highlight = False
        for item in self.get('columns'):
            if item.block_type == 'secondary_highlight':
                has_secondary_highlight = True

        return has_secondary_highlight

    def num_columns(self):
        """Count number of columns."""
        return max(3, len(self.get('columns')))

    def num_columns_max(self):
        """Count maximum columns."""
        max_num = 4
        num_cols = self.num_columns()
        if num_cols > max_num:
            num_cols = ceil(num_cols / 2)
        return num_cols

    def num_rows(self):
        """Count number of rows."""
        num_rows = 1
        if self.has_secondary() and self.num_columns() > 3:
            num_rows = 2
        return num_rows

    def num_columns_row(self):
        """Count maximum rows."""
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
        """Define container class."""
        return 'l-%sup' % str(self.num_columns_row())

    def column_class(self):
        """Define column class."""
        return 'l-%sup__col' % str(self.num_columns_row())


class TransStructValue(StructValue):
    """Class for a struct value that enables translation outside of Django Modeltranslation."""

    def description(self):
        """Fetch translated definition."""
        return get_localised_field_value(
            self,
            'description',
            use_get=True,
        )

    def title(self):
        """Fetch translated title."""
        return get_localised_field_value(
            self,
            'title',
            use_get=True,
        )

    def link_label(self):
        """Fetch translated link label."""
        return get_localised_field_value(
            self,
            'link_label',
            use_get=True,
        )
