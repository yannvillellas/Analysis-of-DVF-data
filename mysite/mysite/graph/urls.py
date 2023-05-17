from django.urls import path

from . import views

urlpatterns = [
    path("", views.homepage, name="homepage"),
    path("graph/", views.homepage, name="homepage"),
    path("prixMoyen/<str:region>", views.prixMoyen, name="prixMoyenRegions"),
    path("nombreVentes/<str:region>", views.nombreVentes, name="nombreVentesRegions"),
    path("tailleMoyenne/<str:region>", views.tailleMoyenne, name="tailleMoyenneRegions"),
    path("prixNombrePieces/<str:region>", views.prixNombrePieces, name="prixNombrePiecesRegions"),
    path("progressionVentes/<str:region>", views.progressionVentes, name="progressionVentesRegions"),

]