from django.shortcuts import render
# from django.http import HttpResponse
# from django.template import loader
from django.shortcuts import render
from django import forms
import pandas as pd
import plotly.express as px
import requests

# Create your views here.

# On importe le fichier csv
dvf2022 = pd.read_csv("valeursfoncieres-2022.txt", sep="|", low_memory=False)

#Suppression des colonnes inutiles pour les demandes des valeurs foncières de 2022
dvf2022 = dvf2022.drop(['Identifiant de document', 'Reference document', '1 Articles CGI', '2 Articles CGI', '3 Articles CGI', '4 Articles CGI','5 Articles CGI', 'No disposition', 'No voie'], axis=1)
dvf2022 = dvf2022.drop(['B/T/Q', 'Type de voie', 'Code voie', 'Code commune', 'Prefixe de section', 'Section', 'No plan', 'No Volume'], axis=1)
dvf2022 = dvf2022.drop(['Voie','Nature culture speciale', 'Identifiant local', 'Nombre de lots', '3eme lot', 'Surface Carrez du 3eme lot', '5eme lot', 'Surface Carrez du 5eme lot', '4eme lot', 'Surface Carrez du 4eme lot'], axis=1)

#ValueError: could not convert string to float: '55000,00'
dvf2022['Valeur fonciere'] = dvf2022['Valeur fonciere'].str.replace(',', '.').astype(float)

#On avait une erreur vu qu'on pouvait pas calculer sur des strings
dvf2022['Surface reelle bati'] = dvf2022['Surface reelle bati'].astype(float)

#On créé une nouvelle colonne qui contient le prix au mètre carré qui est la sormme des Surface Carrez
dvf2022['Surface Carrez du 1er lot'] = dvf2022['Surface Carrez du 1er lot'].str.replace(',', '.').astype(float)
dvf2022['Surface Carrez du 2eme lot'] = dvf2022['Surface Carrez du 2eme lot'].str.replace(',', '.').astype(float)

#On remplace toutes les valeurs nulles par 0
dvf2022 = dvf2022.fillna(0)

#On créé une nouvelle colonne qui contient le prix au mètre carré qui est la sormme des Surface Carrez
dvf2022['Metre carre'] = dvf2022['Surface Carrez du 1er lot'].astype(float) + dvf2022['Surface Carrez du 2eme lot'].astype(float)

#Enleve les valeurs en double
dvf2022 = dvf2022.drop_duplicates(subset=['Date mutation', 'Valeur fonciere', 'Surface reelle bati', 'Metre carre'], keep='first')

# On fait un nouveau tableau contenant que des "Metre carre" non nuls
dvf2022_metre_carre = dvf2022[dvf2022['Metre carre'] >= 1]

#On remplace le nom des communes avec un - par un espace
dvf2022_metre_carre['Commune'] = dvf2022_metre_carre['Commune'].str.replace('-', ' ')

# class to create a form with a choice field
class MyForm(forms.Form):
    my_choice_field = forms.ChoiceField(choices=[])
    def __init__(self, *args, **kwargs):
        choices = kwargs.pop('choices', [])
        super().__init__(*args, **kwargs)
        self.fields['my_choice_field'].choices = choices

def homepage(request):
    # form avec les choix de plot qui amène sur les pages /prixMoyen et /nombreVente
    list_choices = [('prixMoyen', 'Prix moyen par mètre carré par département en France'), ('nombreVente', 'Nombre de ventes par département en France')]
    form = MyForm(choices=list_choices)
    context = {
        'form': form
    }
    if request.method == 'POST':
        form = MyForm(request.POST, choices=list_choices)
        if form.is_valid():
            choice = form.cleaned_data['my_choice_field']
            if choice == 'prixMoyen':
                return prixMoyen(request)
            elif choice == 'nombreVente':
                return nombreVente(request)
    return render(request, 'homepage.html', context)

def prixMoyen(request):
    moyenne_prix_metre_carre_departement = dvf2022_metre_carre.groupby('Code departement')['Valeur fonciere'].mean() / dvf2022_metre_carre.groupby('Code departement')['Metre carre'].mean()

    #On renomme les colonnes
    moyenne_prix_metre_carre_departement = moyenne_prix_metre_carre_departement.reset_index()
    moyenne_prix_metre_carre_departement = moyenne_prix_metre_carre_departement.rename(columns={'Code departement': 'Département', 0: 'Prix moyen au mètre carré'})

    #On fait un geojson avec les départements
    departement_geojson_url = "https://france-geojson.gregoiredavid.fr/repo/departements.geojson"
    departement_geojson = requests.get(departement_geojson_url).json()


    fig = px.choropleth(moyenne_prix_metre_carre_departement, 
                        geojson=departement_geojson, 
                        locations='Département', 
                        color='Prix moyen au mètre carré',
                        color_continuous_scale='pinkyl',
                        featureidkey='properties.code',
                        projection="mercator",
                        title='Prix moyen par mètre carré par département en France')
    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(height=600, width=800)
    
    plot_html = fig.to_html(full_html=False, default_height=500, default_width=700)
    # template = loader.get_template("template0.html")
    context = {
        "plot": plot_html
    }
    # return HttpResponse(template.render(context, request))
    return render(request, "plot.html", context)

def nombreVente(request):
    nombre_de_vente_par_departement = dvf2022.groupby('Code departement')['Valeur fonciere'].count()

    #On renomme les colonnes
    nombre_de_vente_par_departement = nombre_de_vente_par_departement.reset_index()
    nombre_de_vente_par_departement = nombre_de_vente_par_departement.rename(columns={'Code departement': 'Département', 'Valeur fonciere': 'Nombre de ventes'})

    #On fait un geojson avec les départements
    departement_geojson_url = "https://france-geojson.gregoiredavid.fr/repo/departements.geojson"
    departement_geojson = requests.get(departement_geojson_url).json()


    fig = px.choropleth(nombre_de_vente_par_departement, 
                        geojson=departement_geojson, 
                        locations='Département', 
                        color='Nombre de ventes',
                        color_continuous_scale='pinkyl',
                        featureidkey='properties.code',
                        projection="mercator",
                        title='Nombre de ventes par département en France')
    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(height=600, width=800)

    plot_html = fig.to_html(full_html=False, default_height=500, default_width=700)
    context = {
        "plot": plot_html
    }
    return render(request, "plot.html", context)