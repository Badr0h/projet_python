from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    # Home and core pages
    path('', views.HomeView.as_view(), name='home'),
    path('item/<int:pk>/', views.ItemDetailView.as_view(), name='item-detail'),
    path('add/', views.AddItemView.as_view(), name='add-item'),
    
    # Authentication URLs
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # User profile and dashboard
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('dashboard/', views.dashboard, name='dashboard'),
    
    # Reservation
    path('item/<int:pk>/reserve/', views.reservation_view, name='reserve-item'),
    
    # Password reset URLs
    path('password_reset/', 
        views.CustomPasswordResetView.as_view(), 
        name='password_reset'
    ),
    path('password_reset/done/', 
        views.CustomPasswordResetDoneView.as_view(), 
        name='password_reset_done'
    ),
    path('reset/<uidb64>/<token>/', 
        views.CustomPasswordResetConfirmView.as_view(), 
        name='password_reset_confirm'
    ),
    path('reset/done/', 
        views.CustomPasswordResetCompleteView.as_view(), 
        name='password_reset_complete'
    ),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
