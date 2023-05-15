from django.urls import path

from . import views

urlpatterns = [
    path("", views.homepage, name="homepage"),
    path("graph/", views.homepage, name="homepage"),
    path("prixMoyen/", views.prixMoyen, name="prixMoyen"),
    path("nombreVente/", views.nombreVente, name="nombreVente"),
    path("regions/", views.regionsChoice, name="regions"),
    path("regions/", views.regionsChoice, name="regions"),
    path("auvergne-rhone-alpes/", views.AuvergneRhôneAlpes, name="auvergne_rhone_alpes"),
    # path("bourgogne-franche-comte/", views.BourgogneFrancheComte, name="bourgogne_franche_comte"),
    # path("bretagne/", views.Bretagne, name="bretagne"),
    # path("centre-val-de-loire/", views.CentreValDeLoire, name="centre_val_de_loire"),
    # path("corse/", views.Corse, name="corse"),
    # path("grand-est/", views.GrandEst, name="grand_est"),
    # path("hauts-de-france/", views.HautsDeFrance, name="hauts_de_france"),
    # path("ile-de-france/", views.IleDeFrance, name="ile_de_france"),
    # path("normandie/", views.Normandie, name="normandie"),
    # path("nouvelle-aquitaine/", views.NouvelleAquitaine, name="nouvelle_aquitaine"),
    # path("occitanie/", views.Occitanie, name="occitanie"),
    # path("pays-de-la-loire/", views.PaysDeLaLoire, name="pays_de_la_loire"),
    # path("provence-alpes-cote-dazur/", views.ProvenceAlpesCoteDAzur, name="provence_alpes_cote_dazur"),
]