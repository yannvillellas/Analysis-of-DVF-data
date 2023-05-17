from django.urls import path

from . import views

urlpatterns = [
    path("", views.homepage, name="homepage"),
    path("graph/", views.homepage, name="homepage"),
    path("prixMoyen/", views.prixMoyen, name="prixMoyen"),
    path("nombreVente/", views.nombreVente, name="nombreVente"),
    path("regionsForm/", views.regionsForm, name="regionsForm"),
    path("regionsPlot/", views.regionsPlot, name="regionsPlot"),
    path("regionsPlot/<str:region>", views.regionsPlot, name="regionsPlot"),
    path("regionsFormPlot/", views.regionsFormPlot, name="regionsFormPlot"),
    path("regionsFormPlot/<str:region>", views.regionsFormPlot, name="regionsFormPlot"),
]