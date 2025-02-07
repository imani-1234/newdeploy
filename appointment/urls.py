from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RegisterView, LoginView, DoctorViewSet, PatientViewSet, AppointmentViewSet

from django.urls import path
from .views import LoggedInPatientView, DoctorViewSet, AppointmentViewSet, PatientViewSet

router = DefaultRouter()
router.register(r'doctors', DoctorViewSet)
router.register(r'patients', PatientViewSet)
router.register(r'appointments', AppointmentViewSet)

urlpatterns = [
    path('', include(router.urls)),
    
    path('patients/me/', LoggedInPatientView.as_view(), name='logged-in-patient'),
    path('doctors/', DoctorViewSet.as_view({'get': 'list'}), name='doctor-list'),
    path('appointments/', AppointmentViewSet.as_view({'post': 'create'}), name='appointment-create'),
]
