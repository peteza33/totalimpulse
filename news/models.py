import uuid

from django.db import models

class NewsPost(models.Model):
	id = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
	company_name = models.CharField(max_length = 50)
	title = models.CharField(max_length = 250)
	url = models.URLField(max_length = 500)
	sector = models.CharField(max_length = 250) # Launch, In-Space, etc
	tech = models.CharField(max_length = 250) # FEEP, Hall, ADN, HAN, Hydrazine, etc
	category = models.CharField(max_length = 250) # Chemical or Electric
	created = models.DateTimeField(auto_now_add = True)
	modified = models.DateTimeField(auto_now = True)
	published = models.DateField(null = True)