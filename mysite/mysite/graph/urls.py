from django.urls import path

from . import views

urlpatterns = [
    path("", views.homepage, name="homepage"),
    path("graph/", views.homepage, name="homepage"),
    # path("prixMoyen/", views.prixMoyen, name="prixMoyen"),
    path("prixMoyen/<str:region>", views.prixMoyenRegions, name="prixMoyenRegions"),
    # path("nombreVente/", views.nombreVente, name="nombreVente"),
    path("nombreVentes/<str:region>", views.nombreVentesRegions, name="nombreVentesRegions"),
]