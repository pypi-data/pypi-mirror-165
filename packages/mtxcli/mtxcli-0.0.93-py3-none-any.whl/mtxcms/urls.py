from django.urls import include, path
from django.contrib import admin
from django.urls import path
from django.views.decorators.csrf import csrf_exempt
# from graphene_django.views import GraphQLView
# from wagtail.admin import urls as wagtailadmin_urls
from django.conf.urls.i18n import i18n_patterns
from django.conf import settings
# from wagtail.core import urls as wagtail_urls
# from . import views
# from grapple import urls as grapple_urls
from django.contrib.auth.models import User
from rest_framework import serializers, viewsets, routers
# from mtxauth.views import UserViewSet

# Routers provide a way of automatically determining the URL conf.
# router = routers.DefaultRouter()
# router.register(r'users', UserViewSet)
# from .schema import schema
urlpatterns = [
    path('admin/', admin.site.urls),
    # path('api/', include(router.urls)), # rest_api
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    # path("adminbd123/", view=views.adminbd, name="base_admindb"),
    path('oauth/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    path("demo/", include("demo.urls")),
    # path('api/graphql/', csrf_exempt(GraphQLView.as_view())),
    # path('api/graphiql/', csrf_exempt(GraphQLView.as_view(graph!@#iql=True, pretty=True))),
    # path('graphql/', csrf_exempt(GraphQLView.as_view(schema=schema, graphiql=True,pretty=True))),    
    # path('wagadmin/', include(wagtailadmin_urls), name="wagadmin"),
    path("auth/",include("mtxauth.urls")),
    # http://localhost:8801/grapple/graphql/ 为标准的graphql后端，目前用作练习。和对比自定义的graphql 的功能差异。
    # path("grapple/", include(grapple_urls)),
    # path("", include(grapple_urls)),
    path('mtx_cloud/',include('mtx_cloud.urls')),
    path('gallery/',include('gallery.urls'))
    # path("auth0demo/",include("auth0authorization.urls")),
]


urlpatterns = urlpatterns + i18n_patterns(
    # 这所包含的path，都会根据浏览器的语言自动跳转到对应的网址前缀，例如/en/
    # path("search/", search_views.search, name="search"),
    # For anything not caught by a more specific rule above, hand over to
    # Wagtail's page serving mechanism. This should be the last pattern in
    # the list:
    # path("", include(wagtail_urls)),
    # Alternatively, if you want Wagtail pages to be served from a subpath
    # of your site, rather than the site root:
    #    path("pages/", include(wagtail_urls)),
)

if hasattr(settings,"LOCAL_DEV"):
    # 本机开发版，静态文件由本机处理。
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    # from django.views.generic import TemplateView
    # from django.views.generic.base import RedirectView

    # Serve static and media files from development server
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

