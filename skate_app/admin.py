from django.contrib import admin
from .models import Student, Trainer, Training, Schedule, Price


# Register your models here.

class StudentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'balance')
    search_fields = ('name', 'email', 'phone')
    list_filter = ('balance',)


class TrainerAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'rate')
    search_fields = ('name', 'email', 'phone')
    list_filter = ('rate',)


class TrainingAdmin(admin.ModelAdmin):
    list_display = ('trainer', 'date', 'start_time', 'end_time', 'max_students')
    search_fields = ('trainer__name', 'date')
    list_filter = ('trainer', 'date')
    filter_horizontal = ('students',)


class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('date', 'start_time', 'end_time', 'price')
    search_fields = ('date',)
    list_filter = ('date', 'price')


class PriceAdmin(admin.ModelAdmin):
    list_display = ('training_price', 'free_hour_price')


admin.site.register(Student, StudentAdmin)
admin.site.register(Trainer, TrainerAdmin)
admin.site.register(Training, TrainingAdmin)
admin.site.register(Schedule, ScheduleAdmin)
admin.site.register(Price, PriceAdmin)
