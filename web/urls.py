from django.conf.urls.static import static
from django.conf import settings
from django.urls import path
from .views import (
    HomeView,
    AboutView,
    TypeListView,
    TypeSearch,
    TypeCreateView,
    TypeUpdateView,
    TypeDeleteView,
    SigListView,
    SigCreateView,
    SigUpdateView,
    SigDeleteView,
    SigSearch,
)

urlpatterns = [
    path('', HomeView.as_view(), name='sigma-home'),
    path('type/search/', TypeSearch.as_view(), name='type-search'),
    path('type/', TypeListView.as_view(), name='type-list'),
    path('type/new/', TypeCreateView.as_view(), name='type-create'),
    path('type/<int:pk>/update/', TypeUpdateView.as_view(), name='type-update'),
    path('type/<int:pk>/delete/', TypeDeleteView.as_view(), name='type-delete'),
    path('sig/', SigListView.as_view(), name='sig-list'),
    path('sig/search/', SigSearch.as_view(), name='sig-search'),
    path('sig/new/', SigCreateView.as_view(), name='sig-create'),
    path('sig/<int:pk>/update/', SigUpdateView.as_view(), name='sig-update'),
    path('sig/<int:pk>/delete/', SigDeleteView.as_view(), name='sig-delete'),
    path('about/', AboutView.as_view(), name='sigma-about'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
