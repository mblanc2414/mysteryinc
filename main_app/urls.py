from django.urls import path
from . import views 
urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('characters/', views.characters_index, name='index'),
    path('characters/<int:characters_id>/', views.characters_detail, name='detail'),
    path('characters/create', views.CharacterCreate.as_view(), name='characters_create'),
    path('characters/<int:pk>/update/', views.CharacterUpdate.as_view(), name='Characters_update'),
    path('characters/<int:pk>/delete/', views.CharacterDelete.as_view(), name='Characters_delete'),
    path('characters/<int:characters_id>/add_unmasked/', views.add_unmasked, name='add_unmasked'),
    path('character/<int:characters_id>/add_photo/', views.add_photo, name='add_photo'),
    path('accounts/signup/', views.signup, name='signup'),
]