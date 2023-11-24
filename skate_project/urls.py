from django.contrib import admin
from django.urls import path, include
from skate_app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('students/', views.StudentListView.as_view(), name='student-list'),
    path('students/<int:pk>/', views.StudentDetailView.as_view(), name='student-detail'),
    path('trainers/', views.TrainerListView.as_view(), name='trainer-list'),
    path('trainers/<int:pk>/', views.TrainerDetailView.as_view(), name='trainer-detail'),
    path('trainings/', views.TrainingListView.as_view(), name='training-list'),
    path('trainings/<int:pk>/', views.TrainingDetailView.as_view(), name='training-detail'),
    path('trainings/new/', views.TrainingCreateView.as_view(), name='training-create'),
    path('trainings/<int:pk>/update/', views.TrainingUpdateView.as_view(), name='training-update'),
    path('trainings/<int:pk>/delete/', views.TrainingDeleteView.as_view(), name='training-delete'),
    path('trainings/<int:pk>/register/', views.training_register, name='training-register'),
    path('trainings/<int:pk>/cancel/', views.training_cancel, name='training-cancel'),
    path('schedules/', views.ScheduleListView.as_view(), name='schedule-list'),
    path('schedules/<int:pk>/', views.ScheduleDetailView.as_view(), name='schedule-detail'),
    path('schedules/new/', views.ScheduleCreateView.as_view(), name='schedule-create'),
    path('schedules/<int:pk>/update/', views.ScheduleUpdateView.as_view(), name='schedule-update'),
    path('schedules/<int:pk>/delete/', views.ScheduleDeleteView.as_view(), name='schedule-delete'),
    path('schedules/<int:pk>/book/', views.schedule_book, name='schedule-book'),
    path('prices/', views.PriceListView.as_view(), name='price-list'),
    path('prices/<int:pk>/', views.PriceDetailView.as_view(), name='price-detail'),
    path('prices/new/', views.PriceCreateView.as_view(), name='price-create'),
    path('prices/<int:pk>/update/', views.PriceUpdateView.as_view(), name='price-update'),
    path('prices/<int:pk>/delete/', views.PriceDeleteView.as_view(), name='price-delete'),
    path('generate_report/', views.generate_report_view, name='generate-report'),
    path('backup_data/', views.backup_data_view, name='backup-data'),
    path('accounts/', include('django.contrib.auth.urls')),
]