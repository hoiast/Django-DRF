from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from employee_review.models import Employee, Review, Feedback
from django.contrib.auth.models import User
import json


class AdminAPITestCase(APITestCase):

    def setUp(self):

        self.employee1 = Employee.objects.create(name='John')
        self.employee2 = Employee.objects.create(name='Jane')
        self.employee3 = Employee.objects.create(name='Clark')
        self.review = Review.objects.create(
            employee=self.employee1,
            title='This is a review for employee 1',
            review='Employee 1 has been a horrible employee'
        )
        self.feedback1 = Feedback.objects.create(
            employee=self.employee2,
            review=self.review,
            pending=True,
            feedback=''
        )
        self.feedback2 = Feedback.objects.create(
            employee=self.employee3,
            review=self.review,
            pending=False,
            feedback='Good Review'
        )

        self.employee_list_url = reverse('admin-employee-list')
        self.employee1_detail_url = reverse(
            'admin-employee-detail', kwargs={'pk': self.employee1.id})
        self.review_list_url = reverse('admin-review-list')
        self.review1_detail_url = reverse(
            'admin-review-detail', kwargs={'pk': self.review.id})
        self.feedback_list_url = reverse('admin-feedback')

    def authenticate(self):
        user = User.objects.create(username='root')
        user.set_password('123')
        self.client.force_authenticate(user=user)

    def test_employee_unauthenticated(self):
        response = self.client.get(self.employee_list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_employee_authenticated_get(self):
        self.authenticate()
        response = self.client.get(self.employee_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)
        self.assertEqual(response.data[0]['name'], 'John')

    def test_employee_authenticated_post(self):
        self.authenticate()
        response = self.client.post(self.employee_list_url, {'name': 'Mark'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], 'Mark')

    def test_employee_authenticated_get_detail(self):
        self.authenticate()
        response = self.client.get(self.employee1_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'John')

    def test_employee_authenticated_put(self):
        self.authenticate()
        response = self.client.put(
            self.employee1_detail_url, {'name': 'Bruce'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Bruce')

    def test_employee_authenticated_patch(self):
        self.authenticate()
        response = self.client.patch(
            self.employee1_detail_url, {'name': 'Bruce'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Bruce')

    def test_employee_authenticated_delete(self):
        self.authenticate()
        response = self.client.delete(self.employee1_detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_review_unauthenticated(self):
        response = self.client.get(self.review_list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_review_authenticated_get(self):
        self.authenticate()
        response = self.client.get(self.review_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'],
                         'This is a review for employee 1')

    def test_review_authenticated_post(self):
        self.authenticate()
        data = {
            'employee': 'John',
            'title': 'This is a new review for employee',
            'review': 'Employee 1 has been a horrible employee again'
        }
        response = self.client.post(self.review_list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'],
                         'This is a new review for employee')

    def test_review_authenticated_get_detail(self):
        self.authenticate()
        response = self.client.get(self.review1_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'],
                         'This is a review for employee 1')

    def test_review_authenticated_put(self):
        self.authenticate()
        response = self.client.put(self.review1_detail_url, {
            'employee': 'Jane',
            'title': 'This is a new review for employee 1',
            'review': 'Employee 1 has been a horrible employee again'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'],
                         'This is a new review for employee 1')

    def test_review_authenticated_patch(self):
        self.authenticate()
        response = self.client.patch(self.review1_detail_url, {
            'employee': 'Clark',
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['employee'], 'Clark')

    def test_review_authenticated_delete(self):
        self.authenticate()
        response = self.client.delete(self.review1_detail_url)
        self.assertEqual(response.status_code,
                         status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_feedback_unauthenticated(self):
        response = self.client.get(self.feedback_list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_feedback_authenticated_get(self):
        self.authenticate()
        response = self.client.get(self.feedback_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['feedback'], '')

    def test_feedback_authenticated_post(self):
        self.authenticate()
        response = self.client.post(self.feedback_list_url, json.dumps({
            'review': self.review.id,
            'employee': 'Clark',
        }), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['pending'], True)
        self.assertEqual(response.data['feedback'], '')
