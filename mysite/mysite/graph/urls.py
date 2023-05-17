from django.urls import path

from . import views

urlpatterns = [
    path("", views.homepage, name="homepage"),
    path("graph/", views.homepage, name="homepage"),
    path("prixMoyen/", views.prixMoyen, name="prixMoyen"),
    path("nombreVente/", views.nombreVente, name="nombreVente"),
    path("regionsForm/", views.regionsForm, name="regionsForm"),
    path("regionsFormPlot/", views.regionsFormPlot, name="regionsFormPlot"),
    path("regionsPlot/", views.regionsPlot, name="regionsPlot"),
]