
from django.test import TestCase
from employee_review.models import Employee, Review, Feedback


class FixturesTestCase(TestCase):
    fixtures = ['employee_review/fixtures/data.json']

    def test_employee(self):
        employee = Employee.objects.get(id=1)
        self.assertEqual(employee.name, 'John')

    def test_review(self):
        review = Review.objects.get(id=1)
        self.assertEqual(review.title, 'This is a review for employee 1')
        self.assertEqual(
            review.review, 'Employee 1 has been a horrible employee')

    def test_pending_feedback(self):
        feedback = Feedback.objects.get(id=1)
        self.assertEqual(feedback.pending, True)
        self.assertEqual(feedback.feedback, '')

    def test_not_pending_feedback(self):
        feedback = Feedback.objects.get(id=5)
        self.assertEqual(feedback.pending, False)
        self.assertEqual(feedback.feedback, 'Good Review')
