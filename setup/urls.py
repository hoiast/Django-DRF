from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from employee_review.views import \
    AdminEmployeeViewSet, \
    AdminReviewViewSet, \
    AdminFeedbackView, \
    PublicEmployeeViewSet, \
    PublicReviewViewSet, \
    PublicListFeedbackView, \
    PublicFeedbackView, \
    PublicListPendingFeedbacksEmployee

adminRouter = routers.DefaultRouter()
adminRouter.register(r'employees', AdminEmployeeViewSet,
                     basename='admin-employee')
adminRouter.register(r'reviews', AdminReviewViewSet, basename='admin-review')

publicRouter = routers.DefaultRouter()
publicRouter.register(r'employees', PublicEmployeeViewSet)
publicRouter.register(r'reviews', PublicReviewViewSet)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/admin/', include(adminRouter.urls)),
    path('api/admin/feedbacks', AdminFeedbackView.as_view(), name='admin-feedback'),
    path('api/', include(publicRouter.urls)),
    path('api/employees/<int:pk>/pending-feedbacks',
         PublicListPendingFeedbacksEmployee.as_view(), name='employee-pending-feedbacks'),
    path('api/feedbacks', PublicListFeedbackView.as_view(), name='feedback-list'),
    path('api/feedbacks/<int:pk>',
         PublicFeedbackView.as_view(), name='feedback-detail'),
]


# Swagger Documentation
schema_view = get_schema_view(
    openapi.Info(
        title="Employee Reviews API",
        default_version='v1',
        description="API to access employee reviews and provide feedbacks",
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns.extend([
    path('swagger/', schema_view.with_ui('swagger',
         cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc',
                                       cache_timeout=0), name='schema-redoc'),
])
