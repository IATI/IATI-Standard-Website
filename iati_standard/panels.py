"""Module for bespoke panel definitions."""
from django.forms.widgets import Select
from wagtail.admin.panels import FieldPanel
from iati_standard.edit_handlers import MultiFieldPanel


def ReferenceDataPanel(
    heading='Data settings',
    description='''
        Configuration settings for the reference data.
        Select which tag should be used to populate the IATI Standard reference section.<br><br>
        <strong>Please note: when updating, transferring new data takes time - please be patient, and do not refresh or leave the page until the process has completed.</strong>
        <div id="profile-data-controls">
            <p>
                <button type="button" class="button action-update-profile-data button-longrunning" data-tag="ssot" data-clicked-text="Updating SSOT data…">
                    <span class="icon icon-spinner"></span>
                    <em>Update SSOT data</em>
                </button>
                <button type="button" class="button action-update-profile-data button-longrunning" data-tag="guidance" data-clicked-text="Updating guidance data…">
                    <span class="icon icon-spinner"></span>
                    <em>Update guidance data</em>
                </button>
                <button type="button" class="button action-update-profile-data button-longrunning" data-tag="developer" data-clicked-text="Updating developer data…">
                    <span class="icon icon-spinner"></span>
                    <em>Update developer data</em>
                </button>
            </p>
            <div class="messages">
                <ul></ul>
            </div>
        </div>
    '''
):
    """Define a panel with a button to update the page hierarchy."""
    return MultiFieldPanel(
        [
            FieldPanel('live_tag'),
            FieldPanel('repo'),
        ],
        heading=heading,
        description=description
    )
