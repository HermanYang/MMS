from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += patterns('',
    url(r'^image_search$', 'ir.views.search'),
    url(r'^image_search_result/(?P<algoritham>\w+)/(?P<file>\w+.\w+)$', 'ir.views.search_result'),
)

urlpatterns += patterns('',
    url(r'^register_ik_images$', 'ik.views.register_images'),
    url(r'^knowledge_list$', 'ik.views.list'),
    url(r'^knowledge_editing/(?P<id>\d+)$', 'ik.views.editing'),
    url(r'^knowledge_deletion/(?P<id>\d+)$', 'ik.views.deletion'),
)

urlpatterns += patterns('',
    url(r'^image_knowledge_search$', 'ikr.views.search'),
    url(r'^image_knowledge_search_result/(?P<algoritham>\w+)/(?P<file>\w+.\w+)$', 'ikr.views.search_result'),
)

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
