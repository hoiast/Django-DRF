from django.db import models


class Employee(models.Model):
    name = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Review(models.Model):
    employee = models.ForeignKey(
        Employee, on_delete=models.CASCADE)  # who is being reviewed
    title = models.CharField(max_length=100)
    review = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.review


class Feedback(models.Model):
    review = models.ForeignKey(Review, on_delete=models.CASCADE)
    # who is giving the feedback
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    pending = models.BooleanField(default=True)
    feedback = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.feedback
