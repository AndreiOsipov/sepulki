from django.urls import path

from .views import ShmurdickView, GrymzickView, FufelnitsaView, LoginRedirectView


urlpatterns = [
    path("shmurdik", ShmurdickView.as_view(), name="shmurdik"),
    path("grymzik", GrymzickView.as_view(), name="grymzik"),
    path("fufelnitsa", FufelnitsaView.as_view(), name="fufelnitsa"),
    path("kanban_login", LoginRedirectView.as_view(), name='kanban_login')
]