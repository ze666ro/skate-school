from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Student, Trainer, Training, Schedule, Price


# Create your tests here.

class SkateAppTestCase(TestCase):

    def setUp(self):
        # Create a user, a student and a trainer
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.student = Student.objects.create(user=self.user, name='Test Student', email='test@student.com',
                                              phone='1234567890', balance=100)
        self.trainer = Trainer.objects.create(user=self.user, name='Test Trainer', email='test@trainer.com',
                                              phone='0987654321', rate=50)
        # Create a training, a schedule and a price
        self.training = Training.objects.create(trainer=self.trainer, date='2023-12-01', start_time='10:00',
                                                end_time='11:00', max_students=10)
        self.schedule = Schedule.objects.create(date='2023-12-02', start_time='12:00', end_time='13:00', price=20)
        self.price = Price.objects.create(training_price=40, free_hour_price=10)
        # Create a client
        self.client = Client()

    def test_student_list_view(self):
        # Login as the user
        self.client.login(username='testuser', password='testpass')
        # Get the response from the student list view
        response = self.client.get(reverse('student-list'))
        # Check the status code, the template used and the context data
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'skate_app/student_list.html')
        self.assertQuerysetEqual(response.context['students'], [repr(self.student)])

    def test_trainer_list_view(self):
        # Login as the user
        self.client.login(username='testuser', password='testpass')
        # Get the response from the trainer list view
        response = self.client.get(reverse('trainer-list'))
        # Check the status code, the template used and the context data
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'skate_app/trainer_list.html')
        self.assertQuerysetEqual(response.context['trainers'], [repr(self.trainer)])

    def test_training_list_view(self):
        # Login as the user
        self.client.login(username='testuser', password='testpass')
        # Get the response from the training list view
        response = self.client.get(reverse('training-list'))
        # Check the status code, the template used and the context data
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'skate_app/training_list.html')
        self.assertQuerysetEqual(response.context['trainings'], [repr(self.training)])

    def test_schedule_list_view(self):
        # Login as the user
        self.client.login(username='testuser', password='testpass')
        # Get the response from the schedule list view
        response = self.client.get(reverse('schedule-list'))
        # Check the status code, the template used and the context data
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'skate_app/schedule_list.html')
        self.assertQuerysetEqual(response.context['schedules'], [repr(self.schedule)])

    def test_price_list_view(self):
        # Login as the user
        self.client.login(username='testuser', password='testpass')
        # Get the response from the price list view
        response = self.client.get(reverse('price-list'))
        # Check the status code, the template used and the context data
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'skate_app/price_list.html')
        self.assertQuerysetEqual(response.context['prices'], [repr(self.price)])

    def test_training_register_view(self):
        # Login as the user
        self.client.login(username='testuser', password='testpass')
        # Post the data to the training register view
        response = self.client.post(reverse('training-register', args=[self.training.pk]))
        # Check the status code, the messages and the database changes
        self.assertEqual(response.status_code, 302)
        messages = list(response.wsgi_request._messages)
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'You have successfully registered for the training.')
        self.assertIn(self.student, self.training.students.all())

    def test_training_cancel_view(self):
        # Login as the user
        self.client.login(username='testuser', password='testpass')
        # Register the student for the training
        self.training.students.add(self.student)
        # Post the data to the training cancel view
        response = self.client.post(reverse('training-cancel', args=[self.training.pk]))
        # Check the status code, the messages and the database changes
        self.assertEqual(response.status_code, 302)
        messages = list(response.wsgi_request._messages)
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'You have successfully canceled your registration for the training.')
        self.assertNotIn(self.student, self.training.students.all())

    def test_schedule_book_view(self):
        # Login as the user
        self.client.login(username='testuser', password='testpass')
        # Post the data to the schedule book view
        response = self.client.post(reverse('schedule-book', args=[self.schedule.pk]))
        # Check the status code, the messages and the database changes
        self.assertEqual(response.status_code, 302)
        messages = list(response.wsgi_request._messages)
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'You have successfully booked the free hour.')
        self.assertEqual(self.student.balance, 90)

    def test_generate_report_view(self):
        # Login as the user
        self.client.login(username='testuser', password='testpass')
        # Post the data to the generate report view
        response = self.client.post(reverse('generate-report'))
        # Check the status code and the messages
        self.assertEqual(response.status_code, 302)
        messages = list(response.wsgi_request._messages)
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]),
                         'The report is being generated. You will receive an email with the report when it is ready.')

    def test_backup_data_view(self):
        # Login as the user
        self.client.login(username='testuser', password='testpass')
        # Post the data to the backup data view
        response = self.client.post(reverse('backup-data'))
        # Check the status code and the messages
        self.assertEqual(response.status_code, 302)
        messages = list(response.wsgi_request._messages)
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]),
                         'The data is being backed up. You will receive an email with the backup file when it is ready.')
