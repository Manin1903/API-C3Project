from django.urls import path
from .views import ItemsView, ItemDetailView ,UserCreateView ,UserDetailView, UserListView
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('ccc-project/', ItemsView.as_view(), name='ccc_project'),
    path('ccc-project/users/create/', UserCreateView.as_view(), name='user-create'),
    path('ccc-project/users/listUser/', UserListView.as_view(), name='user-lists'),
    path('ccc-project/users/<int:id>/', UserDetailView.as_view(), name='user-detail'),
    path('ccc-project/<int:pk>/', ItemDetailView.as_view(), name='user-update'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)