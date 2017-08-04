from django.db import models

from wagtail.wagtailcore.fields import StreamField
from wagtail.wagtailcore import blocks
from wagtail.wagtailadmin.edit_handlers import FieldPanel, StreamFieldPanel, InlinePanel, MultiFieldPanel
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.wagtailimages.blocks import ImageChooserBlock
from wagtail.wagtaildocs.blocks import DocumentChooserBlock
from wagtail.wagtailembeds.blocks import EmbedBlock

from modelcluster.fields import ParentalKey
from modelcluster.tags import ClusterTaggableManager
from taggit.models import TaggedItemBase

from wagtail.wagtailcore.models import Page, Orderable
from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailsearch import index

class BlogIndexPage(Page):
    intro = RichTextField(blank = True)

    def get_context(self, request):
        # Update context to include only published posts, ordered by reverse-chron
        context = super(BlogIndexPage, self).get_context(request)
        content = self.get_children().live().order_by('-first_published_at')
        context['content'] = content
        return context

    content_panels = Page.content_panels + [
        FieldPanel('intro', classname = "full")
    ]

class BlogPageTag(TaggedItemBase):
	content_object = ParentalKey('BlogPage', related_name = 'tagged_items')

class BlogPage(Page):
	author = models.CharField(max_length = 250)
	date = models.DateField('Post date')
	intro = models.CharField(max_length = 250)
	tags = ClusterTaggableManager(through = BlogPageTag, blank = True)
	body = StreamField([
		('heading', blocks.CharBlock(classname = 'full title')),
		('paragraph', blocks.RichTextBlock()),
		('url', blocks.URLBlock()),
		('date', blocks.DateBlock()),
		('time', blocks.TimeBlock()),
		('page', blocks.PageChooserBlock()),
		('image', ImageChooserBlock()),
		('doc', DocumentChooserBlock()),
		('embed', EmbedBlock()),
	])

	def main_image(self):
		gallery_item = self.gallery_images.first()

		if gallery_item:
		    return gallery_item.image
		else:
		    return None

	search_fields = Page.search_fields + [
		index.SearchField('intro'),
		index.SearchField('body'),
		index.SearchField('author'),
	]

	content_panels = Page.content_panels + [
		MultiFieldPanel([
			FieldPanel('date'),
			FieldPanel('tags'),
			], heading = 'Blog information'),
		FieldPanel('author'),
		FieldPanel('intro'),
		StreamFieldPanel('body'),
	]

class BlogPageGalleryImage(Orderable):
	page = ParentalKey(BlogPage, related_name = 'gallery_images')
	image = models.ForeignKey(
		'wagtailimages.Image', on_delete = models.CASCADE, related_name = '+'
	)
	caption = models.CharField(blank = True, max_length = 250)

	panels = [
	ImageChooserPanel('image'),
	FieldPanel('caption'),
	]

class BlogTagIndexPage(Page):

    def get_context(self, request):
        # Filter by tag
        tag = request.GET.get('tag')
        pages = BlogPage.objects.filter().filter(tags__name = tag)

        # Update template context
        context = super(BlogTagIndexPage, self).get_context(request)
        context['pages'] = pages
        return context