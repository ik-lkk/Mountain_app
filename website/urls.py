from django.conf import settings
from django.urls import path
from .views import HomeView,MountainListView,MountainDetailView,ThemeListView,ThemeDetail,Contact,ContactSuccess,UserLoginView,RegistView,RegistSuccess,UserLogoutView,activate_user,edit_theme,delete_theme
from django.contrib.auth import views as auth_views
app_name = 'website'

EMAIL_HOST_USER = getattr(settings, "EMAIL_HOST_USER", None)

urlpatterns = [
    path('home/',HomeView.as_view(),name="home"),
    path('mountain_list/',MountainListView.as_view(),name="mountain_list"),
    path('mountain_detail/<int:pk>',MountainDetailView.as_view(),name="mountain_detail"),
    path('theme_list/',ThemeListView.as_view(),name="theme_list"),
    path('theme_detail/<int:theme_id>',ThemeDetail.as_view(),name="theme_detail"),
    path('contact/',Contact.as_view(),name="contact"),
    path('contact_success/',ContactSuccess.as_view(),name="contact_success"),
    path('user_login/', UserLoginView.as_view(), name="user_login"),
    path('user_logout/', UserLogoutView.as_view(), name="user_logout"),
    path('regist/', RegistView.as_view(), name="regist"),
    path('activate_user/<uuid:token>',activate_user,name="activate_user"),
    path('regist_success/', RegistSuccess.as_view(), name="regist_success"),
    path('edit_theme/<int:id>', edit_theme, name="edit_theme"),
    path('delete_theme/<int:id>', delete_theme, name="delete_theme"),
    
    
]
