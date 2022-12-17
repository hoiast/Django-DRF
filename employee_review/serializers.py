from rest_framework import serializers
from employee_review.models import Employee, Review, Feedback
from employee_review.validators import validate_length, validate_alpha_length_case, validate_length_case


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ['name']

    def validate(self, attrs):
        errors = {}
        for [field, validator] in [
            ['name', validate_alpha_length_case],
        ]:
            if field in attrs:
                validation_errors = validator(attrs[field])
                if validation_errors:
                    errors[field] = validation_errors
        if errors:
            raise serializers.ValidationError(errors)
        return attrs


class ReviewSerializer(serializers.ModelSerializer):
    employee = serializers.SlugRelatedField(
        slug_field='name', queryset=Employee.objects.all())

    class Meta:
        model = Review
        fields = ['id', 'employee', 'title', 'review']

    def validate(self, attrs):
        errors = {}
        for [field, validator] in [
            ['title', validate_length_case,],
            ['review', validate_length,],
        ]:
            if field in attrs:
                validation_errors = validator(attrs[field])
                if validation_errors:
                    errors[field] = validation_errors
        if errors:
            raise serializers.ValidationError(errors)
        return attrs


class FeedbackSerializer(serializers.ModelSerializer):
    employee = serializers.SlugRelatedField(
        slug_field='name', queryset=Employee.objects.all())
    review = serializers.SlugRelatedField(
        slug_field='id', queryset=Review.objects.all())

    class Meta:
        model = Feedback
        fields = ['id', 'employee', 'review', 'pending', 'feedback']
        extra_kwargs = {
            'employee': {'read_only': True},
            'review': {'read_only': True},
        }

    def validate(self, attrs):
        errors = {}
        for [field, validator] in [
            ['feedback', validate_length,],
        ]:
            if field in attrs:
                validation_errors = validator(attrs[field])
                if validation_errors:
                    errors[field] = validation_errors
        if errors:
            raise serializers.ValidationError(errors)
        return attrs
