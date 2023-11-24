from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models import Student, Trainer, Training, Schedule, Price
from .forms import TrainingForm, ScheduleForm, PriceForm
from .tasks import send_email, generate_report, backup_data


# Create your views here.

class StudentListView(LoginRequiredMixin, ListView):
    model = Student
    template_name = 'skate_app/student_list.html'
    context_object_name = 'students'
    paginate_by = 10

    def get_queryset(self):
        return Student.objects.filter(user=self.request.user)


class StudentDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Student
    template_name = 'skate_app/student_detail.html'
    context_object_name = 'student'

    def test_func(self):
        student = self.get_object()
        return self.request.user == student.user


class TrainerListView(LoginRequiredMixin, ListView):
    model = Trainer
    template_name = 'skate_app/trainer_list.html'
    context_object_name = 'trainers'
    paginate_by = 10

    def get_queryset(self):
        return Trainer.objects.all()


class TrainerDetailView(LoginRequiredMixin, DetailView):
    model = Trainer
    template_name = 'skate_app/trainer_detail.html'
    context_object_name = 'trainer'


class TrainingListView(LoginRequiredMixin, ListView):
    model = Training
    template_name = 'skate_app/training_list.html'
    context_object_name = 'trainings'
    paginate_by = 10

    def get_queryset(self):
        if self.request.user.is_staff:
            return Training.objects.all()
        else:
            return Training.objects.filter(students__user=self.request.user)


class TrainingDetailView(LoginRequiredMixin, DetailView):
    model = Training
    template_name = 'skate_app/training_detail.html'
    context_object_name = 'training'


class TrainingCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Training
    template_name = 'skate_app/training_form.html'
    form_class = TrainingForm

    def test_func(self):
        return self.request.user.is_staff

    def form_valid(self, form):
        form.instance.trainer = Trainer.objects.get(user=self.request.user)
        return super().form_valid(form)


class TrainingUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Training
    template_name = 'skate_app/training_form.html'
    form_class = TrainingForm

    def test_func(self):
        training = self.get_object()
        return self.request.user == training.trainer.user

    def form_valid(self, form):
        form.instance.trainer = Trainer.objects.get(user=self.request.user)
        return super().form_valid(form)


class TrainingDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Training
    template_name = 'skate_app/training_confirm_delete.html'
    success_url = '/trainings/'

    def test_func(self):
        training = self.get_object()
        return self.request.user == training.trainer.user


@login_required
@user_passes_test(lambda u: u.is_staff)
def training_register(request, pk):
    training = get_object_or_404(Training, pk=pk)
    if request.method == 'POST':
        if training.students.count() < training.max_students:
            training.students.add(Student.objects.get(user=request.user))
            messages.success(request, f'You have successfully registered for the training.')
            send_email.delay(request.user.email, f'Confirmation of registration for the training {training}')
        else:
            messages.error(request, f'The training is full. You cannot register for it.')
        return redirect('training-detail', pk=pk)
    else:
        return render(request, 'skate_app/training_register.html', {'training': training})


@login_required
@user_passes_test(lambda u: not u.is_staff)
def training_cancel(request, pk):
    training = get_object_or_404(Training, pk=pk)
    if request.method == 'POST':
        if request.user in training.students.all():
            training.students.remove(Student.objects.get(user=request.user))
            messages.success(request, f'You have successfully canceled your registration for the training.')
            send_email.delay(request.user.email, f'Confirmation of cancellation for the training {training}')
        else:
            messages.error(request, f'You are not registered for this training. You cannot cancel it.')
        return redirect('training-detail', pk=pk)
    else:
        return render(request, 'skate_app/training_cancel.html', {'training': training})


class ScheduleListView(LoginRequiredMixin, ListView):
    model = Schedule
    template_name = 'skate_app/schedule_list.html'
    context_object_name = 'schedules'
    paginate_by = 10

    def get_queryset(self):
        return Schedule.objects.all()


class ScheduleDetailView(LoginRequiredMixin, DetailView):
    model = Schedule
    template_name = 'skate_app/schedule_detail.html'
    context_object_name = 'schedule'


class ScheduleCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Schedule
    template_name = 'skate_app/schedule_form.html'
    form_class = ScheduleForm

    def test_func(self):
        return self.request.user.is_staff


class ScheduleUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Schedule
    template_name = 'skate_app/schedule_form.html'
    form_class = ScheduleForm

    def test_func(self):
        return self.request.user.is_staff


class ScheduleDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Schedule
    template_name = 'skate_app/schedule_confirm_delete.html'
    success_url = '/schedules/'

    def test_func(self):
        return self.request.user.is_staff


@login_required
@user_passes_test(lambda u: not u.is_staff)
def schedule_book(request, pk):
    schedule = get_object_or_404(Schedule, pk=pk)
    if request.method == 'POST':
        student = Student.objects.get(user=request.user)
        price = Price.objects.first()
        if student.balance >= price.free_hour_price:
            student.balance -= price.free_hour_price
            student.save()
            messages.success(request, f'You have successfully booked the free hour.')
            send_email.delay(request.user.email, f'Confirmation of booking the free hour {schedule}')
        else:
            messages.error(request, f'You do not have enough balance to book the free hour.')
        return redirect('schedule-detail', pk=pk)
    else:
        return render(request, 'skate_app/schedule_book.html', {'schedule': schedule})


class PriceListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Price
    template_name = 'skate_app/price_list.html'
    context_object_name = 'prices'
    paginate_by = 10

    def test_func(self):
        return self.request.user.is_staff


class PriceDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Price
    template_name = 'skate_app/price_detail.html'
    context_object_name = 'price'

    def test_func(self):
        return self.request.user.is_staff


class PriceCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Price
    template_name = 'skate_app/price_form.html'
    form_class = PriceForm

    def test_func(self):
        return self.request.user.is_staff


class PriceUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Price
    template_name = 'skate_app/price_form.html'
    form_class = PriceForm

    def test_func(self):
        return self.request.user.is_staff


class PriceDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Price
    template_name = 'skate_app/price_confirm_delete.html'
    success_url = '/prices/'

    def test_func(self):
        return self.request.user.is_staff


@login_required
@user_passes_test(lambda u: u.is_staff)
def generate_report_view(request):
    if request.method == 'POST':
        generate_report.delay()
        messages.success(request,
                         f'The report is being generated. You will receive an email with the report when it is ready.')
        return redirect('home')
    else:
        return render(request, 'skate_app/generate_report.html')


@login_required
@user_passes_test(lambda u: u.is_staff)
def backup_data_view(request):
    if request.method == 'POST':
        backup_data.delay()
        messages.success(request,
                         f'The data is being backed up. You will receive an email with the backup file when it is ready.')
        return redirect('home')
    else:
        return render(request, 'skate_app/backup_data.html')
