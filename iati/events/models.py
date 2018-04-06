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
    
    # Heading
    
    heading = models.CharField(max_length=255,null=True,blank=True)
    
    # Excerpt
    
    excerpt = models.TextField(null=True,blank=True)
    
    @property
    def events(self):
        # Get list of live event pages that are descendents of this page
        events = EventPage.objects.live().descendant_of(self)
        
        # Order by most recent
        events = events.order_by('-date_start')
        
        return events
    
    content_panels_en = [
        MultiFieldPanel([
            FieldPanel('title_en'),
            FieldPanel('heading_en'),
            FieldPanel('excerpt_en')
        ])
    ]
    
    content_panels_fr = [
        MultiFieldPanel([
            FieldPanel('title_fr'),
            FieldPanel('heading_fr'),
            FieldPanel('excerpt_fr')
        ])
    ]
    
    content_panels_es = [
        MultiFieldPanel([
            FieldPanel('title_es'),
            FieldPanel('heading_es'),
            FieldPanel('excerpt_es')
        ])
    ]
    
    content_panels_pt = [
        MultiFieldPanel([
            FieldPanel('title_pt'),
            FieldPanel('heading_pt'),
            FieldPanel('excerpt_pt')
        ])
    ]
    
    edit_handler = TabbedInterface([
        ObjectList(content_panels_en,heading='English content'),
        ObjectList(content_panels_fr,heading='French content'),
        ObjectList(content_panels_es,heading='Spanish content'),
        ObjectList(content_panels_pt,heading='Portuguese content'),
        ObjectList(Page.promote_panels,heading='Promote'),
        ObjectList(Page.settings_panels,heading='Settings',classname='settings')
    ])

class EventPage(Page):
    parent_page_types = ['events.EventIndexPage']
    subpage_types = []

    date_start = models.DateTimeField("Event start date and time")
    date_end = models.DateTimeField("Event end date and time",null=True,blank=True)

    
    location = models.TextField(null=True,blank=True)
    
    registration_link = models.URLField(max_length=255,null=True,blank=True)
    
    heading = models.TextField(null=True,blank=True)
    
    subheading = models.TextField(null=True,blank=True)
    
    description = StreamField(IATIStreamBlock(required=False),null=True,blank=True)
    
    # additional_information
    
    additional_information = StreamField(IATIStreamBlock(required=False),null=True,blank=True)
    
    event_type = ParentalManyToManyField('events.EventType',blank=True)
    
    @property
    def event_type_concat(self):
        event_types = self.event_type.values_list('name', flat=True) 
        
        return " ".join(event_types)
    
    content_panels_multi = [
        MultiFieldPanel([
            FieldPanel('date_start'),
            FieldPanel('date_end'),
            FieldPanel('location'),
            FieldPanel('registration_link'),
        ])
    ]
    content_panels_en = [
        MultiFieldPanel([
            FieldPanel('title_en'),
            FieldPanel('heading_en'),
            FieldPanel('subheading_en')
        ]),
        StreamFieldPanel('description_en'),
        StreamFieldPanel('additional_information_en')
    ]
    
    content_panels_fr = [
        MultiFieldPanel([
            FieldPanel('title_fr'),
            FieldPanel('heading_fr'),
            FieldPanel('subheading_fr')
        ]),
        StreamFieldPanel('description_fr'),
        StreamFieldPanel('additional_information_fr')
    ]
    
    content_panels_es = [
        MultiFieldPanel([
            FieldPanel('title_es'),
            FieldPanel('heading_es'),
            FieldPanel('subheading_es')
        ]),
        StreamFieldPanel('description_es'),
        StreamFieldPanel('additional_information_es')
    ]
    
    content_panels_pt = [
        MultiFieldPanel([
            FieldPanel('title_pt'),
            FieldPanel('heading_pt'),
            FieldPanel('subheading_pt')
        ]),
        StreamFieldPanel('description_pt'),
        StreamFieldPanel('additional_information_pt')
    ]
    
    edit_handler = TabbedInterface([
        ObjectList(content_panels_multi,heading='Multilingual content'),
        ObjectList(content_panels_en,heading='English content'),
        ObjectList(content_panels_fr,heading='French content'),
        ObjectList(content_panels_es,heading='Spanish content'),
        ObjectList(content_panels_pt,heading='Portuguese content'),
        ObjectList(Page.promote_panels,heading='Promote'),
        ObjectList(Page.settings_panels,heading='Settings',classname='settings')
    ])
    
@register_snippet
class EventType(models.Model):
    name = models.CharField(max_length=255)
    
    def __str__(self):
        return self.name
    
    panels = [
        FieldPanel('name'),
    ]
