from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from employee_review.models import Employee, Review, Feedback
from django.contrib.auth.models import User
import json


class PublicAPITestCase(APITestCase):

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

        self.employee_list_url = reverse('employee-list')
        self.employee1_detail_url = reverse(
            'employee-detail', kwargs={'pk': self.employee1.id})
        self.employee2_pending_feedbacks_url = reverse(
            'employee-pending-feedbacks', kwargs={'pk': self.employee2.id})
        self.review_list_url = reverse('review-list')
        self.review1_detail_url = reverse(
            'review-detail', kwargs={'pk': self.review.id})
        self.feedback_list_url = reverse('feedback-list')
        self.feedback1_detail_url = reverse(
            'feedback-detail', kwargs={'pk': self.feedback1.id})

    def test_employee_get(self):
        response = self.client.get(self.employee_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)
        self.assertEqual(response.data[0]['name'], 'John')

    def test_employee_get_detail(self):
        response = self.client.get(self.employee1_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'John')

    def test_employee_pending_feedbacks(self):
        response = self.client.get(self.employee2_pending_feedbacks_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_review_get(self):
        response = self.client.get(self.review_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'],
                         'This is a review for employee 1')

    def test_review_get_detail(self):
        response = self.client.get(self.review1_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'],
                         'This is a review for employee 1')

    def test_feedback_get(self):
        response = self.client.get(self.feedback_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['feedback'], '')

    def test_feedback_get_detail(self):
        response = self.client.get(self.feedback1_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['feedback'], '')

    def test_feedback_patch(self):
        response = self.client.patch(self.feedback1_detail_url, {
                                     'feedback': 'Good Review'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['feedback'], 'Good Review')
