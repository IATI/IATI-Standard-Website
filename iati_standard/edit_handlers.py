"""Module for edit handlers involved in IATI Standards."""

from github import Github
from github import GithubException
from django.conf import settings
from wagtail.admin.panels import MultiFieldPanel as WagtailMultiFieldPanel


DATA_FILENAME = 'output.zip'
MEDIA_FILENAME = 'downloads.zip'


class MultiFieldPanel(WagtailMultiFieldPanel):
    """Replace default MultiFieldPanel with one that can display descriptions."""

    def __init__(self, children=(), *args, **kwargs):
        """Overwrite __init__ method to remove and capture description kwarg."""
        if kwargs.get('description', None):
            self.description = kwargs.pop('description')
        super().__init__(children, *args, **kwargs)

    def clone_kwargs(self):
        """Overwrite clone_kwargs method to populate MultiFieldPanel with additional kwargs."""
        kwargs = super().clone_kwargs()
        if hasattr(self, 'description'):
            kwargs['description'] = self.description
        return kwargs

    class BoundPanel(WagtailMultiFieldPanel.BoundPanel):
        template_name = "wagtailadmin/panels/multi_field_panel.html"

        def __init__(self, panel, instance, request, form, **kwargs):
            """Override __init__ method to include description."""
            super().__init__(panel=panel, instance=instance, request=request, form=form, **kwargs)
            self.description = panel.description


class GithubAPI:
    """Class to connect to Github API."""

    def __init__(self, url=None):
        """Initialize class."""
        self.url = url
        self.org = self.url.split('/')[3]
        self.repo = self.url.split('/')[4]
        self.git = self._git()

    def get_data(self, tag_name):
        """Fetch outputs.zip given a release tag name."""
        if not tag_name:
            raise ValueError('%s must be set to access data' % tag_name)

        data = None
        release = self._get_release(tag_name)
        assets = self._get_assets_for_release(release)
        data = self._get_zip_for_release(assets, DATA_FILENAME)
        media = self._get_zip_for_release(assets, MEDIA_FILENAME)

        return (data, media)

    def get_live_data(self):
        """Fetch outputs.zip given a live tag name."""
        return self._get_data('live_tag')

    def get_draft_data(self):
        """Fetch outputs.zip given a draft tag name."""
        return self._get_data('draft_tag')

    def get_releases(self):
        """Fetch all release tag names."""
        return self._get_repo().get_releases()

    def _git(self):
        """Return Github object."""
        return Github(settings.GITHUB_TOKEN)

    def _get_repo(self):
        """Fetch repository object."""
        try:
            return self.git.get_organization(self.org).get_repo(self.repo)
        except GithubException:
            return self.git.get_user(self.org).get_repo(self.repo)

    def _get_release(self, tag):
        """Fetch specific release."""
        return self._get_repo().get_release(tag)

    def _get_assets_for_release(self, release):
        """Fetch assets for a release."""
        return release.get_assets()

    def _get_zip_for_release(self, assets, name):
        """Fetch zip file for a release."""
        for item in assets:
            if item.content_type == 'application/zip' and item.name == name:
                return item
