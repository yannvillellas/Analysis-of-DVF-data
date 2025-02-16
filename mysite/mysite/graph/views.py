from django.shortcuts import render, redirect
from django import forms
import pandas as pd
import plotly.express as px
import requests

## 2022
# On importe le fichier csv
dvf2022 = pd.read_csv("valeursfoncieres-2022.txt", sep="|", low_memory=False)
# Suppression des colonnes inutiles pour les demandes des valeurs foncières de 2022
dvf2022 = dvf2022.drop(['Identifiant de document', 'Reference document', '1 Articles CGI', '2 Articles CGI', '3 Articles CGI', '4 Articles CGI','5 Articles CGI', 'No disposition', 'No voie'], axis=1)
dvf2022 = dvf2022.drop(['B/T/Q', 'Type de voie', 'Code voie', 'Code commune', 'Prefixe de section', 'Section', 'No plan', 'No Volume'], axis=1)
dvf2022 = dvf2022.drop(['Voie','Nature culture speciale', 'Identifiant local', 'Nombre de lots', '3eme lot', 'Surface Carrez du 3eme lot', '5eme lot', 'Surface Carrez du 5eme lot', '4eme lot', 'Surface Carrez du 4eme lot'], axis=1)
# ValueError: could not convert string to float: '55000,00'
dvf2022['Valeur fonciere'] = dvf2022['Valeur fonciere'].str.replace(',', '.').astype(float)
# On avait une erreur vu qu'on pouvait pas calculer sur des strings
dvf2022['Surface reelle bati'] = dvf2022['Surface reelle bati'].astype(float)
# On créé une nouvelle colonne qui contient le prix au mètre carré qui est la sormme des Surface Carrez
dvf2022['Surface Carrez du 1er lot'] = dvf2022['Surface Carrez du 1er lot'].str.replace(',', '.').astype(float)
dvf2022['Surface Carrez du 2eme lot'] = dvf2022['Surface Carrez du 2eme lot'].str.replace(',', '.').astype(float)
# On remplace toutes les valeurs nulles par 0
dvf2022 = dvf2022.fillna(0)
# On créé une nouvelle colonne qui contient le prix au mètre carré qui est la sormme des Surface Carrez
dvf2022['Metre carre'] = dvf2022['Surface Carrez du 1er lot'].astype(float) + dvf2022['Surface Carrez du 2eme lot'].astype(float)
# Enleve les valeurs en double
dvf2022 = dvf2022.drop_duplicates(subset=['Date mutation', 'Valeur fonciere', 'Surface reelle bati', 'Metre carre'], keep='first')
# On fait un nouveau tableau contenant que des "Metre carre" non nuls
dvf2022_metre_carre = dvf2022[dvf2022['Metre carre'] >= 1]
# On remplace le nom des communes avec un - par un espace
dvf2022_metre_carre['Commune'] = dvf2022_metre_carre['Commune'].str.replace('-', ' ')
#Comparaison du prix moyen du mètre carré entre les différentes régions de France
group_by_department = dvf2022.groupby('Code departement')['Valeur fonciere'].mean() / dvf2022.groupby('Code departement')['Metre carre'].mean()
#On enlève les départements d'outre mer
group_by_department = group_by_department.drop(['971', '972', '973', '974'])
#On regroupe par région
regions = {
    "France": ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10',
            '11', '12', '13', '14', '15', '16', '17', '18', '19', '21',
            '22', '23', '24', '25', '26', '27', '28', '29', '2A', '2B',
            '30', '31', '32', '33', '34', '35', '36', '37', '38', '39',
            '40', '41', '42', '43', '44', '45', '46', '47', '48', '49',
            '50', '51', '52', '53', '54', '55', '56', '57', '58', '59',
            '60', '61', '62', '63', '64', '65', '66', '67', '68', '69',
            '70', '71', '72', '73', '74', '75', '76', '77', '78', '79',
            '80', '81', '82', '83', '84', '85', '86', '87', '88', '89',
            '90', '91', '92', '93', '94', '95'],
    "Auvergne-Rhône-Alpes": ['01', '03', '07', '15', '26', '38', '42', '43', '63', '69', '73', '74'],
    "Bourgogne-Franche-Comté": ['21', '25', '39', '58', '70', '71', '89', '90'],
    "Bretagne": ['22', '29', '35', '56'],
    "Centre-Val de Loire": ['18', '28', '36', '37', '41', '45'],
    "Corse": ['2A', '2B'],
    "Grand Est": ['08', '10', '51', '52', '54', '55', '57', '67', '68', '88'],
    "Hauts-de-France": ['02', '59', '60', '62', '80'],
    "Île-de-France": ['75', '77', '78', '91', '92', '93', '94', '95'],
    "Normandie": ['14', '27', '50', '61', '76'],
    "Nouvelle-Aquitaine": ['16', '17', '19', '23', '24', '33', '40', '47', '64', '79', '86', '87'],
    "Occitanie": ['09', '11', '12', '30', '31', '32', '34', '46', '48', '65', '66', '81', '82'],
    "Pays de la Loire": ['44', '49', '53', '72', '85'],
    "Provence-Alpes-Côte d'Azur": ['04', '05', '06', '13', '83', '84']
}
#On fait un geojson avec les départements
departement_geojson_url = "https://france-geojson.gregoiredavid.fr/repo/departements.geojson"
departement_geojson = requests.get(departement_geojson_url).json()

class MyForm(forms.Form):
    my_choice_field = forms.ChoiceField(choices=[])
    def __init__(self, *args, **kwargs):
        choices = kwargs.pop('choices', [])
        super().__init__(*args, **kwargs)
        self.fields['my_choice_field'].choices = choices


def homepage(request):
    list_choices = [
        ('prixMoyen', 'Prix moyen par mètre carré par département en France'),
        ('nombreVentes', 'Nombre de ventes par département en France'),
        ('tailleMoyenne', 'Taille moyenne des terrains par département en France'),
        ('prixNombrePieces', 'Prix moyen par nombre de pièces principales'),
        ('progressionVentes', 'Évolution de mutation immobilière en France en 2022')
        ]
    form = MyForm(choices=list_choices)
    context = {
        'form': form
    }
    if request.method == 'POST':
        form = MyForm(request.POST, choices=list_choices)
        if form.is_valid():
            choice = form.cleaned_data['my_choice_field']
            if choice == 'prixMoyen':
                response = redirect('/prixMoyen/France')
                return response
            elif choice == 'nombreVentes':
                response = redirect('/nombreVentes/France')
                return response
            elif choice == 'tailleMoyenne':
                response = redirect('/tailleMoyenne/France')
                return response
            elif choice == 'prixNombrePieces':
                response = redirect('/prixNombrePieces/France')
                return response
            elif choice == 'progressionVentes':
                response = redirect('/progressionVentes/France')
                return response
    return render(request, 'form.html', context)


def prixMoyen(request, region):
    list_departements = regions[region]
    dvf2022_metre_carre_region = dvf2022_metre_carre[dvf2022_metre_carre['Code departement'].isin(list_departements)]
    moyenne_prix_metre_carre_departement = dvf2022_metre_carre_region.groupby('Code departement')['Valeur fonciere'].mean() / dvf2022_metre_carre_region.groupby('Code departement')['Metre carre'].mean()
    #On renomme les colonnes
    moyenne_prix_metre_carre_departement = moyenne_prix_metre_carre_departement.reset_index()
    moyenne_prix_metre_carre_departement = moyenne_prix_metre_carre_departement.rename(columns={'Code departement': 'Département', 0: 'Prix moyen au mètre carré'})
    fig = px.choropleth(moyenne_prix_metre_carre_departement,
                        geojson=departement_geojson,
                        locations='Département',
                        color='Prix moyen au mètre carré',
                        color_continuous_scale='pinkyl',
                        featureidkey='properties.code',
                        projection="mercator",
                        title=f'Prix moyen par mètre carré en {region}')
    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(height=600, width=800)
    plot_html = fig.to_html(full_html=False, default_height=500, default_width=700)

    list_choices = [ (key, key) for key in regions.keys() ]
    form = MyForm(choices=list_choices)
    if request.method == 'POST':
        form = MyForm(request.POST, choices=list_choices)
        if form.is_valid():
            choice = form.cleaned_data['my_choice_field']
            response = redirect('/prixMoyen/' + choice)
            return response
    context = {
        "form": form,
        "plot": plot_html
    }
    return render(request, "formplot.html", context)


def nombreVentes(request, region):
    list_departements = regions[region]
    dvf2022_region = dvf2022[dvf2022['Code departement'].isin(list_departements)]
    nombre_de_vente_par_departement = dvf2022_region.groupby('Code departement')['Valeur fonciere'].count()
    #On renomme les colonnes
    nombre_de_vente_par_departement = nombre_de_vente_par_departement.reset_index()
    nombre_de_vente_par_departement = nombre_de_vente_par_departement.rename(columns={'Code departement': 'Département', 'Valeur fonciere': 'Nombre de ventes'})
    fig = px.choropleth(nombre_de_vente_par_departement,
                        geojson=departement_geojson,
                        locations='Département',
                        color='Nombre de ventes',
                        color_continuous_scale='pinkyl',
                        featureidkey='properties.code',
                        projection="mercator",
                        title=f'Nombre de ventes en {region}')
    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(height=600, width=800)
    plot_html = fig.to_html(full_html=False, default_height=500, default_width=700)

    list_choices = [ (key, key) for key in regions.keys() ]
    form = MyForm(choices=list_choices)
    if request.method == 'POST':
        form = MyForm(request.POST, choices=list_choices)
        if form.is_valid():
            choice = form.cleaned_data['my_choice_field']
            response = redirect('/nombreVentes/' + choice)
            return response
    context = {
        "form": form,
        "plot": plot_html
    }
    return render(request, "formplot.html", context)

def tailleMoyenne(request, region):
    list_departements = regions[region]
    dvf2022_region = dvf2022[dvf2022['Code departement'].isin(list_departements)]
    moyenne_taille_terrain = dvf2022_region[dvf2022_region['Surface terrain'] > 0]
    moyenne_taille_terrain = moyenne_taille_terrain.groupby('Code departement')['Surface terrain'].mean()
    #On renomme les colonnes
    moyenne_taille_terrain = moyenne_taille_terrain.reset_index()
    moyenne_taille_terrain = moyenne_taille_terrain.rename(columns={'Code departement': 'Département', 0: 'Surface moyenne du terrain'})
    fig = px.choropleth(moyenne_taille_terrain, 
                        geojson=departement_geojson, 
                        locations='Département', 
                        color='Surface terrain',
                        color_continuous_scale='blugrn',
                        featureidkey='properties.code',
                        projection="mercator",
                        title='Surface moyenne des terrains par département en France')
    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(height=600, width=800)
    plot_html = fig.to_html(full_html=False, default_height=500, default_width=700)

    list_choices = [ (key, key) for key in regions.keys() ]
    form = MyForm(choices=list_choices)
    if request.method == 'POST':
        form = MyForm(request.POST, choices=list_choices)
        if form.is_valid():
            choice = form.cleaned_data['my_choice_field']
            response = redirect('/tailleMoyenne/' + choice)
            return response
    context = {
        "form": form,
        "plot": plot_html
    }
    return render(request, "formplot.html", context)

def prixNombrePieces(request, region):
    list_departements = regions[region]
    dvf2022_region = dvf2022[dvf2022['Code departement'].isin(list_departements)]
    prix_par_piece = dvf2022_region.query("`Nombre pieces principales`.notna() and `Nombre pieces principales` != 0")
    prix_par_piece = prix_par_piece.groupby('Nombre pieces principales')['Valeur fonciere'].mean()
    #On enlève les valeurs supérieurs à 20 pièces
    prix_par_piece = prix_par_piece[prix_par_piece.index <= 20]
    #On renomme les colonnes
    prix_par_piece = prix_par_piece.reset_index()
    prix_par_piece = prix_par_piece.rename(columns={'Nombre pieces principales': 'Nombre de pièces principales', 'Valeur fonciere': 'Prix moyen'})
    fig = px.bar(prix_par_piece, x='Nombre de pièces principales', y='Prix moyen', title='Prix moyen par nombre de pièces principales')
    plot_html = fig.to_html(full_html=False, default_height=500, default_width=700)

    list_choices = [ (key, key) for key in regions.keys() ]
    form = MyForm(choices=list_choices)
    if request.method == 'POST':
        form = MyForm(request.POST, choices=list_choices)
        if form.is_valid():
            choice = form.cleaned_data['my_choice_field']
            response = redirect('/prixNombrePieces/' + choice)
            return response
    context = {
        "form": form,
        "plot": plot_html
    }
    return render(request, "formplot.html", context)


def progressionVentes(request, region):
    list_departements = regions[region]
    dvf2022_region = dvf2022[dvf2022['Code departement'].isin(list_departements)]
    ventes_par_jours = dvf2022_region
    ventes_par_jours['Date mutation'] = pd.to_datetime(ventes_par_jours['Date mutation'], format='%d/%m/%Y')
    ventes_par_jours = ventes_par_jours.groupby(pd.Grouper(key='Date mutation', freq='M')).size().reset_index(name='Nombre de ventes')
    ventes_par_jours.sort_values('Date mutation', inplace=True)
    fig = px.line(ventes_par_jours, x='Date mutation', y='Nombre de ventes', title=f'Évolution de mutation immobilière en {region} en 2022')
    plot_html = fig.to_html(full_html=False, default_height=500, default_width=700)

    list_choices = [ (key, key) for key in regions.keys() ]
    form = MyForm(choices=list_choices)
    if request.method == 'POST':
        form = MyForm(request.POST, choices=list_choices)
        if form.is_valid():
            choice = form.cleaned_data['my_choice_field']
            response = redirect('/progressionVentes/' + choice)
            return response
    context = {
        "form": form,
        "plot": plot_html
    }
    return render(request, "formplot.html", context)