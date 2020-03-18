"""Module for edit handlers involved in IATI Standards."""

from github import Github
from github import GithubException
from django.conf import settings
from wagtail.admin.edit_handlers import FieldPanel
from wagtail.admin.edit_handlers import MultiFieldPanel as WagtailMultiFieldPanel


DATA_FILENAME = 'output.zip'


class MultiFieldPanel(WagtailMultiFieldPanel):
    """Replace default MultiFieldPanel with one that can display descriptions."""

    def __init__(self, children=(), *args, **kwargs):
        """Overwrite __init__ method to remove and capture description kwarg."""
        if kwargs.get('description', None):
            self.description = kwargs.pop('description')
        super().__init__(children, *args, **kwargs)

    def clone(self):
        """Overwrite clone method to populate MultiFieldPanel with additional kwargs."""
        props = {
            'children': self.children,
            'heading': self.heading,
            'classname': self.classname,
            'help_text': self.help_text,
        }
        if hasattr(self, 'description'):
            props['description'] = self.description
        return self.__class__(**props)


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

        return data

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


class TagFieldPanel(FieldPanel):
    """Replacement FieldPanel that auto-populates with tagged releases."""

    def get_releases(self, repo):
        """Fetch release names given a repo."""
        git = GithubAPI(repo)
        return [(x.tag_name, x.tag_name) for x in git.get_releases()]

    def on_form_bound(self):
        """Overwrite on_form_bound to populate choices."""
        try:
            choices = self.get_releases(self.instance.repo) if self.instance.repo else []
            self.form.fields[self.field_name].widget.choices = choices
            self.form.fields[self.field_name].empty_label = None
        except Exception:
            pass

        super().on_form_bound()
