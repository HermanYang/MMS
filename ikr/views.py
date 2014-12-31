from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.shortcuts import redirect 
from django.shortcuts import render
from django.template import RequestContext
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
		return render(request, 'image_knowledge_search.html', context_instance = RequestContext(request))

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

		return redirect('/image_knowledge_search_result/{0}/{1}'.format(feature_algorithm, filename + extension))

def search_result(request, algoritham, file):
	args= {}

	if request.method == 'GET':
		filename, extension = os.path.splitext(file)
		feature_algorithm = algoritham

		HOME = os.getenv('HOME')
		IMAGE_RETRIEVAL_SYSTEM_BACKEND_PATH = os.getenv('IMAGE_RETRIEVAL_SYSTEM_BACKEND_PATH')
		IMAGE_KNOWLEDGE_RETRIEVAL_SYSTEM_DATA_PATH = os.getenv('IMAGE_KNOWLEDGE_RETRIEVAL_SYSTEM_DATA_PATH')

		path = os.path.join(MEDIA_ROOT, 'images', filename + extension)

		output_path = os.path.join( HOME, 'tmp')
		config_file = os.path.join(IMAGE_KNOWLEDGE_RETRIEVAL_SYSTEM_DATA_PATH, 'voctree_config', '{0}'.format(feature_algorithm))
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
		tag_dict = {}
		offset = 5
		
		for line in result_file:
			image = {}
			result_image_name = line.split()[0]
			result_score = int(line.split()[1])
			result_score = result_score * offset
			offset = offset * 0.9
			url = '/static/ikr_images/{0}'.format(result_image_name + '.jpg')
			image['url'] = url
			image_list.append(image)

			image_obj = Image.objects.get(name = result_image_name + '.jpg')
			image_knowledge_obj_list = ImageKnowledge.objects.filter( image_id = image_obj.id )

			for obj in image_knowledge_obj_list:
				knowledge_objcet = Knowledge.objects.get( id = obj.knowledge_id ) 
				if knowledge_objcet.description not in tag_dict:
					tag_dict[ knowledge_objcet.description ] = result_score
				else:
					tag_dict[ knowledge_objcet.description ] += result_score

			if count > 100:
				break;

			count += 1

		best_score = None
		result_tag = ''
		print tag_dict

		for tag in tag_dict:
			if best_score != None:
				if tag_dict[tag] > best_score: 
					best_score = tag_dict[tag]
					result_tag = tag
			else:
				best_score = tag_dict[tag]
				result_tag = tag


		args['image_list'] = image_list
		args['tag'] = result_tag

		return render(request, 'image_knowledge_search_result.html', args, context_instance = RequestContext(request))
