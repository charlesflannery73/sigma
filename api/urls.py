from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework.schemas import get_schema_view
from rest_framework.documentation import include_docs_urls

from .views import TypeViewSet, SigViewSet


router = DefaultRouter()
router.register('v1/type', TypeViewSet, 'api_type_list')
router.register('v1/sig', SigViewSet, 'api_sig_list')
schema_view = get_schema_view(title='Sigma API',
                              description='An API to query types and signatures',
                              version=1
                              )


urlpatterns = [
    path('api/', include(router.urls)),
    path('api/schema/', schema_view),
    path('api/docs/', include_docs_urls(title='Sigma API')),
]
