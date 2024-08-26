from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [

    path('homepage/',views.homepage_view, name='homepage'),
    path('hotel/', views.hotel_list_view, name='hotel_list'),
    path('hotel/<int:hotel_id>/', views.hotel_detail_view, name='hotel_detail'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='logout.html'), name='logout'),
    path('signup/', views.signup, name='signup'),
    path('show_bookings/', views.show_bookings, name='show_bookings'),
    path('show_bookings_results/', views.show_bookings, name='show_bookings_results'),
    path('reserve_confirmation/<int:room_id>/', views.reserve_confirmation, name='reserve_confirmation'),
    path('my_bookings/', views.my_bookings, name='my_bookings'),
    path('delete_booking/<int:booking_id>/', views.delete_booking, name='delete_booking'),
    path('recommendation/', views.recommend_room, name='recommend_room'),
    path('chatbot/', views.index, name='index'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 