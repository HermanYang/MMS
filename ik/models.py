from django.db import models

# Create your models here.

class Knowledge(models.Model):
	description = models.CharField(max_length=30)
	
	class Meta:
		db_table = 'knowledge'


class Image(models.Model):
	name = models.CharField(max_length=30)

	class Meta:
		db_table = 'image'

class ImageKnowledge(models.Model):
	image_id = models.IntegerField()
	knowledge_id = models.IntegerField()

	class Meta:
		db_table = 'image_knowledge'


