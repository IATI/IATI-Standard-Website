"""Application configuration for the governance app."""

from django.apps import AppConfig


class GovernanceConfig(AppConfig):
    """Config class for the governance app."""

    name = 'governance'

    def ready(self):
        """Override ready method to perform initialization tasks."""
        from .models import MembersAssemblyPage
        from .admin import MemberResource

        def members_csv(self):
            members = self.members(order='name')
            export = MemberResource().export(members).subset(cols=['name', 'date_joined', 'url'])
            if export:
                return export.csv
            return ""

        MembersAssemblyPage.members_csv = members_csv
