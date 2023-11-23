from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student')
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return self.name


class Trainer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='trainer')
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    rate = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return self.name


class Training(models.Model):
    trainer = models.ForeignKey(Trainer, on_delete=models.CASCADE, related_name='trainings')
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    students = models.ManyToManyField(Student, related_name='trainings', blank=True)
    max_students = models.PositiveIntegerField(default=10)

    def __str__(self):
        return f"{self.trainer.name} - {self.date} - {self.start_time} - {self.end_time}"


class Schedule(models.Model):
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.date} - {self.start_time} - {self.end_time} - {self.price}"


class Price(models.Model):
    training_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    free_hour_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"Training price: {self.training_price}, Free hour price: {self.free_hour_price}"



