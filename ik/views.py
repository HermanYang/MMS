from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.shortcuts import render
from django.shortcuts import redirect 
from django.template import RequestContext
from django.http import HttpResponse
from mms.settings import MEDIA_ROOT
from mms.settings import BASE_DIR
from models import *

import os
import time
import hashlib
import subprocess

def list(request):
	args = {}
	knowledge_list = []
	if request.method == 'GET':
		obj_list = Knowledge.objects.all()

		for obj in obj_list:
			knowledge = {}
			knowledge['id'] = obj.id
			knowledge['description'] = obj.description
			knowledge_list.append(knowledge)

		args['knowledge_list'] = knowledge_list
		return render(request, 'knowledge_list.html', args, context_instance = RequestContext(request))

	if request.method == 'POST':
		if( len(Knowledge.objects.filter(description = request.POST['knowledge'])) == 0 ):
			knowledge = Knowledge(description = request.POST['knowledge'])
			knowledge.save()

		obj_list = Knowledge.objects.all()

		for obj in obj_list:
			knowledge = {}
			knowledge['id'] = obj.id
			knowledge['description'] = obj.description
			knowledge_list.append(knowledge)

		args['knowledge_list'] = knowledge_list

		return render(request, 'knowledge_list.html', args, context_instance = RequestContext(request))

def register_images(request):
	Image.objects.all().delete()
	path = os.path.join(BASE_DIR, 'statics', 'ik_images')
	file_list =  os.listdir(path)

	for file in file_list:
		print file
		image = Image(name = file)
		image.save()

	return HttpResponse('Succeed')

def editing(request, id):
	args = {}
	image_list = []
	related_image_id_list = []

	if request.method == 'GET':
		knowledge_image_obj = ImageKnowledge.objects.filter(knowledge_id = id)

		for obj in knowledge_image_obj:
			related_image_id_list.append(obj.image_id)

		obj_list = Image.objects.all()

		for obj in obj_list:
			image = {}
			image['url'] = '/static/ik_images/{0}'.format(obj.name)
			image['name'] = obj.name
			image['id'] = obj.id

			if obj.id in related_image_id_list:
				image['related'] = 'checked'

			image_list.append(image)

		args['image_list'] = image_list
		args['knowledge'] = Knowledge.objects.get(id = id)

		return render(request, 'knowledge_editing.html', args, context_instance = RequestContext(request))

	if request.method == 'POST':
		related_image_id_list = request.POST.getlist('related_image')
		image_knowledge_obj_list = ImageKnowledge.objects.filter(knowledge_id = id)

		#delete not related image
		for obj in image_knowledge_obj_list:
			if obj.image_id not in related_image_id_list:
				obj.delete()

		#add related image
		for image_id in related_image_id_list:

			if len(ImageKnowledge.objects.filter(image_id = image_id, knowledge_id = id)) == 0:
				image_knowledge = ImageKnowledge(image_id = image_id, knowledge_id = id)
				image_knowledge.save()

		
		args['redirect_url'] = '/knowledge_editing/{0}'.format(id)
		return render(request, 'success.html', args, context_instance = RequestContext(request))

def deletion(request, id):
	knowledge_obj_list = Knowledge.objects.filter(id = id)
	knowledge_obj_list.delete()

	image_knowledge_obj_list = ImageKnowledge.objects.filter(knowledge_id = id)
	image_knowledge_obj_list.delete()

	return redirect('/knowledge_list')
