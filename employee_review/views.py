from rest_framework import viewsets, generics
from employee_review.models import Employee, Review, Feedback
from employee_review.serializers import EmployeeSerializer, ReviewSerializer, FeedbackSerializer
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


class AdminEmployeeViewSet(viewsets.ModelViewSet):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    http_method_names = ['get', 'post', 'put', 'patch', 'delete']


class AdminReviewViewSet(viewsets.ModelViewSet):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    http_method_names = ['get', 'post', 'put', 'patch']


class AdminFeedbackView(generics.ListCreateAPIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer


class PublicEmployeeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer


class PublicReviewViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer


class PublicListFeedbackView(generics.ListAPIView):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer


class PublicFeedbackView(generics.RetrieveUpdateAPIView):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer
    http_method_names = ['get', 'patch']

    def patch(self, request, pk):
        feedback = Feedback.objects.get(pk=pk)

        # check if the feedback is pending
        if not feedback.pending:
            return Response(status=400, data="feedback is not pending")

        # check if feedback is not empty
        if not request.data['feedback']:
            return Response(status=400, data="feedback cannot be empty")

        # Change pending to false and add feedback
        data = {
            'pending': False,
            'feedback': request.data['feedback']
        }

        serializer = self.get_serializer(feedback, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(status=200, data=serializer.data)
        return Response(status=400, data=serializer.errors)


class PublicListPendingFeedbacksEmployee(generics.ListAPIView):
    serializer_class = FeedbackSerializer

    def get_queryset(self):
        return Feedback.objects.filter(pending=True, employee_id=self.kwargs['pk'])
