from django.urls import path
# from graphene_django.views import GraphQLView

from django.urls import include, path
from django.contrib import admin
from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from . import views
# from . import schema

# schema = schema.create_schema()

urlpatterns = [
    path('', views.index, name='index'),
    path('protected/', views.protected_page,name="protected_page"),
    # path('graphql/', csrf_exempt(GraphQLView.as_view(schema=schema.schema, graphiql=True,pretty=True))),
]
