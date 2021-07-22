"""Application configuration for the governance app."""

from django.apps import AppConfig


class GovernanceConfig(AppConfig):
    """Config class for the governance app."""

    name = 'governance'

    def ready(self):
        """Override ready method to perform initialization tasks."""
        from .models import MembersAssemblyPage
        from .admin import MemberResource

        members = MembersAssemblyPage().members(order='name')
        export = MemberResource().export(members).subset(cols=['name', 'date_joined', 'url'])
        if export:
            MembersAssemblyPage.members_csv = export.csv
