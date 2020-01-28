from github import Github
from django.conf import settings
from wagtail.admin.edit_handlers import FieldPanel
from wagtail.admin.edit_handlers import MultiFieldPanel as WagtailMultiFieldPanel


DATA_FILENAME = 'outputs.zip'


class MultiFieldPanel(WagtailMultiFieldPanel):
    def __init__(self, children=(), *args, **kwargs):
        if kwargs.get('description', None):
            self.description = kwargs.pop('description')
        super().__init__(children, *args, **kwargs)

    def clone(self):
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

    def __init__(self, url=None):
        self.url = url
        self.org = self.url.split('/')[3]
        self.repo = self.url.split('/')[4]
        self.git = self._git()

    def get_data(self, tag_name):
        if not tag_name:
            raise ValueError('%s must be set to access data' % tag_name)

        data = None
        release = self._get_release(tag_name)
        assets = self._get_assets_for_release(release)
        data = self._get_zip_for_release(assets, DATA_FILENAME)

        return data

    def get_live_data(self):
        return self._get_data('live_tag')

    def get_draft_data(self):
        return self._get_data('draft_tag')

    def get_releases(self):
        return self._get_repo().get_releases()

    def _git(self):
        return Github(settings.GITHUB_TOKEN)

    def _get_repo(self):
        return self.git.get_organization(self.org).get_repo(self.repo)

    def _get_release(self, tag):
        return self._get_repo().get_release(tag)

    def _get_assets_for_release(self, release):
        return release.get_assets()

    def _get_zip_for_release(self, assets, name):
        for item in assets:
            if item.content_type == 'application/zip' and item.name == name:
                return item


class TagFieldPanel(FieldPanel):

    def get_releases(self, repo):
        git = GithubAPI(repo)
        return [(x.tag_name, x.tag_name) for x in git.get_releases()]

    def on_form_bound(self):

        try:
            choices = self.get_releases(self.instance.repo) if self.instance.repo else []
            self.form.fields[self.field_name].widget.choices = choices
            self.form.fields[self.field_name].empty_label = None
        except Exception:
            pass

        super().on_form_bound()
