from django.urls import path
from .views import user_list_create, user_detail_update_delete, user_crud_page
 
urlpatterns = [
    path('api/users/', user_list_create),
    path('api/users/<int:user_id>/', user_detail_update_delete),
    path('users-ui/', user_crud_page),

]
