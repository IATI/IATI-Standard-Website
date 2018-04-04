from django.db import models
from wagtail.core.models import Page
from home.models import TranslatedField, IATIStreamBlock
from wagtail.admin.edit_handlers import TabbedInterface, ObjectList, FieldPanel, MultiFieldPanel, StreamFieldPanel
from modelcluster.fields import ParentalManyToManyField
from wagtail.core.fields import StreamField
from wagtail.snippets.models import register_snippet
from django.utils import translation


class EventIndexPage(Page):
    parent_page_types = ['home.HomePage']
    subpage_types = ['events.EventPage']
    
    heading_en = models.CharField(max_length=255,null=True,blank=True)
    heading_fr = models.CharField(max_length=255,null=True,blank=True)
    heading_sp = models.CharField(max_length=255,null=True,blank=True)
    
    heading = TranslatedField(
        'heading_en',
        'heading_fr',
        'heading_sp'
    )
    
    excerpt_en = models.TextField(null=True,blank=True)
    excerpt_fr = models.TextField(null=True,blank=True)
    excerpt_sp = models.TextField(null=True,blank=True)
    
    excerpt = TranslatedField(
        'excerpt_en',
        'excerpt_fr',
        'excerpt_sp'
    )
    
    content_panels_en = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('heading_en'),
            FieldPanel('excerpt_en')
        ])
    ]
    
    content_panels_fr = [
        MultiFieldPanel([
            FieldPanel('heading_fr'),
            FieldPanel('excerpt_fr')
        ])
    ]
    
    content_panels_sp = [
        MultiFieldPanel([
            FieldPanel('heading_sp'),
            FieldPanel('excerpt_sp')
        ])
    ]
    
    @property
    def events(self):
        # Get list of live event pages that are descendents of this page
        events = EventPage.objects.live().descendant_of(self)
        
        # Order by most recent
        events = events.order_by('-date_start')
        
        return events
    
    
    edit_handler = TabbedInterface([
        ObjectList(content_panels_en,heading='English content'),
        ObjectList(content_panels_fr,heading='French content'),
        ObjectList(content_panels_sp,heading='Spanish content'),
        ObjectList(Page.promote_panels,heading='Promote'),
        ObjectList(Page.settings_panels,heading='Settings',classname='settings')
    ])
    
    

class EventPage(Page):
    parent_page_types = ['events.EventIndexPage']
    subpage_types = []
    # Start and end dates, needs at least a start date
    
    date_start = models.DateTimeField("Event start date and time")
    date_end = models.DateTimeField("Event end date and time",null=True,blank=True)
    
    # Location
    
    location = models.TextField(null=True,blank=True)
    
    # Registration link
    
    registration_link = models.URLField(max_length=255,null=True,blank=True)
    
    # Heading
    
    heading_en = models.TextField(null=True,blank=True)
    heading_fr = models.TextField(null=True,blank=True)
    heading_sp = models.TextField(null=True,blank=True)
    
    heading = TranslatedField(
        'heading_en',
        'heading_fr',
        'heading_sp'
    )
    
    # Subheading
    
    subheading_en = models.TextField(null=True,blank=True)
    subheading_fr = models.TextField(null=True,blank=True)
    subheading_sp = models.TextField(null=True,blank=True)
    
    subheading = TranslatedField(
        'subheading_en',
        'subheading_fr',
        'subheading_sp'
    )
    
    # Description
    
    description_en = StreamField(IATIStreamBlock(required=False),null=True,blank=True)
    description_fr = StreamField(IATIStreamBlock(required=False),null=True,blank=True)
    description_sp = StreamField(IATIStreamBlock(required=False),null=True,blank=True)
    
    description = TranslatedField(
        'description_en',
        'description_fr',
        'description_sp'
    )
    
    # additional_information
    
    additional_information_en = StreamField(IATIStreamBlock(required=False),null=True,blank=True)
    additional_information_fr = StreamField(IATIStreamBlock(required=False),null=True,blank=True)
    additional_information_sp = StreamField(IATIStreamBlock(required=False),null=True,blank=True)
    
    additional_information = TranslatedField(
        'additional_information_en',
        'additional_information_fr',
        'additional_information_sp'
    )
    
    event_type = ParentalManyToManyField('events.EventType',blank=True)
    
    @property
    def event_type_concat(self):
        if translation.get_language() == 'fr':
            event_types = self.event_type.values_list('name_fr', flat=True) 
        elif translation.get_language() == 'sp':
            event_types = self.event_type.values_list('name_sp', flat=True) 
        #The default
        else:
            event_types = self.event_type.values_list('name_en', flat=True) 
        
        return " ".join(event_types)
    
    content_panels_en = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('date_start'),
            FieldPanel('date_end'),
            FieldPanel('location'),
            FieldPanel('registration_link'),
            FieldPanel('heading_en'),
            FieldPanel('subheading_en')
        ]),
        StreamFieldPanel('description_en'),
        StreamFieldPanel('additional_information_en')
    ]
    
    content_panels_fr = [
        MultiFieldPanel([
            FieldPanel('heading_fr'),
            FieldPanel('subheading_fr')
        ]),
        StreamFieldPanel('description_fr'),
        StreamFieldPanel('additional_information_fr')
    ]
    
    content_panels_sp = [
        MultiFieldPanel([
            FieldPanel('heading_sp'),
            FieldPanel('subheading_sp')
        ]),
        StreamFieldPanel('description_fr'),
        StreamFieldPanel('additional_information_fr')
    ]
    
    edit_handler = TabbedInterface([
        ObjectList(content_panels_en,heading='English content'),
        ObjectList(content_panels_fr,heading='French content'),
        ObjectList(content_panels_sp,heading='Spanish content'),
        ObjectList(Page.promote_panels,heading='Promote'),
        ObjectList(Page.settings_panels,heading='Settings',classname='settings')
    ])
    
@register_snippet
class EventType(models.Model):
    name_en = models.CharField(max_length=255)
    name_fr = models.CharField(max_length=255,null=True,blank=True)
    name_sp = models.CharField(max_length=255,null=True,blank=True)
    
    name = TranslatedField(
        'name_en',
        'name_fr',
        'name_sp'
    )
    
    def __str__(self):
        return self.name
    
    panels = [
        FieldPanel('name_en'),
        FieldPanel('name_fr'),
        FieldPanel('name_sp')
    ]
