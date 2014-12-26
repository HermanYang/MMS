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

# Create your views here.
def search(request):
	args= {}

	if request.method == 'GET':
		return render(request, 'search.html', context_instance = RequestContext(request))

	if request.method == 'POST':
		feature_algorithm = request.POST['feature_algorithm']
		search_image = request.FILES['search_image']

		filename, extension = os.path.splitext(search_image.name)
		filename = filename + str( time.time() * 1000 )
		md5 = hashlib.md5()
		md5.update(filename)
		filename = str(md5.hexdigest()) 

		IMAGE_RETRIEVAL_SYSTEM_BACKEND_PATH = os.getenv('IMAGE_RETRIEVAL_SYSTEM_BACKEND_PATH')

		path = os.path.join(MEDIA_ROOT, 'images', filename + extension)
		file = open(path, 'wb+')
		file.write(search_image.read())

		return redirect('/image_search_result/{0}/{1}'.format(feature_algorithm, filename + extension))

def search_result(request, algoritham, file):
	args= {}

	if request.method == 'GET':
		filename, extension = os.path.splitext(file)
		feature_algorithm = algoritham

		HOME = os.getenv('HOME')
		IMAGE_RETRIEVAL_SYSTEM_BACKEND_PATH = os.getenv('IMAGE_RETRIEVAL_SYSTEM_BACKEND_PATH')

		path = os.path.join(MEDIA_ROOT, 'images', filename + extension)

		output_path = os.path.join( HOME, 'tmp')
		config_file = os.path.join(IMAGE_RETRIEVAL_SYSTEM_BACKEND_PATH, 'config', 'voctree_{0}.config'.format(feature_algorithm))
		query_bash = os.path.join(IMAGE_RETRIEVAL_SYSTEM_BACKEND_PATH, 'query.sh')

		query_command = '{query_bash} {feature_algorithm} {image_id} {image_path} {voctree_config_file} {output_path}'.format(
				query_bash = query_bash ,feature_algorithm = feature_algorithm, image_id = filename, image_path = path, voctree_config_file = config_file, output_path = output_path
				)

		query_process = subprocess.Popen(query_command, shell = True)
		query_process.wait()

		result_file_path = os.path.join(output_path, '{image_id}_{feature_algorithm}_voctree.txt'.format(
			image_id = filename, feature_algorithm = feature_algorithm)
			)

		result_file = open(result_file_path, 'r')

		image_list = []

		count = 0
		for line in result_file:
			image = {}
			result_image_name = line.split()[0]
			url = '/static/images/{0}'.format(result_image_name + '.jpg')
			image['url'] = url
			image_list.append(image)
			count += 1
			if count > 20:
				break;

		args['image_list'] = image_list

		return render(request, 'search_result.html', args, context_instance = RequestContext(request))

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
		return render(request, 'list.html', args, context_instance = RequestContext(request))

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

		return render(request, 'list.html', args, context_instance = RequestContext(request))

def register_images(request):
	Image.objects.all().delete()
	path = os.path.join(BASE_DIR, 'statics', 'ik_images')
	file_list =  os.listdir(path)

	for file in file_list:
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

		return render(request, 'editing.html', args, context_instance = RequestContext(request))

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
