from django.urls import path
from .views import ItemsView, ItemDetailView ,UserCreateView ,UserDetailView, UserListView ,ItemByUUIDView, ItemDeleteByUUID
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('ccc-project/', ItemsView.as_view(), name='ccc_project'),
    path('ccc-project/users/create/', UserCreateView.as_view(), name='user-create'),
    path('ccc-project/users/listUser/', UserListView.as_view(), name='user-lists'),
    path('ccc-project/users/<int:id>/', UserDetailView.as_view(), name='user-detail'),
    path('ccc-project/<int:pk>/', ItemDetailView.as_view(), name='user-update'),
    path('ccc-project/uuid/<uuid:uuid>/', ItemByUUIDView.as_view(), name='item-by-uuid'),
    path('ccc-project/deleteUserSubmit/<uuid:uuid>/delete/', ItemDeleteByUUID.as_view() , name= 'deleteItem-by-uuid')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)   