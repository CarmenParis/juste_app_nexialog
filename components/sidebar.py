# components/sidebar.py
# Composant de barre latérale avec sélection et configuration de filtres

from dash import html, dcc, callback, Input, Output, State, ALL, MATCH
import dash_bootstrap_components as dbc
from styles.theme import sidebar_styles, sfr_colors
from utils.data_loader import DataManager
import json
from datetime import datetime, date

def create_sidebar():
    """
    Crée la barre latérale de filtres pour l'application
    Returns:
        Composant html.Div contenant la barre latérale
    """
    return html.Div([
        # En-tête de la barre latérale
        html.Div([
            html.I(className="fas fa-filter", style={'marginRight': '10px', 'color': sfr_colors['red']}),
            "Filtres"
        ], style=sidebar_styles['header']),

        # Store pour les filtres sélectionnés
        dcc.Store(id='selected-filter-categories', data=[]),
        
        # Store pour les valeurs des filtres configurés
        dcc.Store(id='filter-values', data={}),

        # Contenu de la barre latérale 
        html.Div([
            # Sélection initiale des filtres (visible par défaut)
            html.Div([
                html.Div([
                    html.I(className="fas fa-cog", style={'marginRight': '8px', 'color': sfr_colors['red']}),
                    "Personnalisation des filtres"
                ], style=sidebar_styles['section_title']),
                
                # Filtres techniques - Structure
                html.Div([
                    html.Label("Filtres techniques – Structure", style=sidebar_styles['label']),
                    dcc.Dropdown(
                        id='filtres-structure',
                        options=[
                            {"label": "Département", "value": "Département"},
                            {"label": "Boucle", "value": "Boucle"},
                            {"label": "Identifiant de PEAG", "value": "Identifiant de PEAG"},
                            {"label": "Identifiant d'OLT", "value": "Identifiant d'OLT"},
                            {"label": "PEBIB", "value": "PEBIB"},
                            {"label": "POP DNS", "value": "POP DNS"}
                        ],
                        multi=True,
                        placeholder="Sélectionnez des filtres...",
                        style=sidebar_styles['dropdown']
                    ),
                ], style=sidebar_styles['filter_section']),
                
                # Filtres techniques - Attributs
                html.Div([
                    html.Label("Filtres techniques – Attributs", style=sidebar_styles['label']),
                    dcc.Dropdown(
                        id='filtres-attributs',
                        options=[
                            {"label": "Nouvelle boucle", "value": "Nouvelle boucle"},
                            {"label": "Modèle d'OLT", "value": "Modèle d'OLT"},
                            {"label": "Nombre de clients", "value": "Nombre de clients"},
                            {"label": "DSP 1", "value": "DSP 1"},
                            {"label": "DEP_PEAG_OLT_match", "value": "DEP_PEAG_OLT_match"}
                        ],
                        multi=True,
                        placeholder="Sélectionnez des filtres...",
                        style=sidebar_styles['dropdown']
                    ),
                ], style=sidebar_styles['filter_section']),
                
                # Filtres temporels
                html.Div([
                    html.Label("Filtres temporels", style=sidebar_styles['label']),
                    dcc.Dropdown(
                        id='filtres-temporels',
                        options=[
                            {"label": "Date", "value": "Date"},
                            {"label": "Heure", "value": "Heure"},
                            {"label": "Jour de la semaine", "value": "Jour de la semaine"},
                            {"label": "Week-end", "value": "Week-end"},
                            {"label": "Heure de nuit", "value": "Heure de nuit"},
                            {"label": "Heure ouvrée", "value": "Heure ouvrée"},
                            {"label": "Jour férié", "value": "Jour férié"},
                            {"label": "Heure de pointe", "value": "Heure de pointe"}
                        ],
                        multi=True,
                        placeholder="Sélectionnez des filtres...",
                        style=sidebar_styles['dropdown']
                    ),
                ], style=sidebar_styles['filter_section']),
                
                # Bouton pour valider la sélection des filtres
                html.Div([
                    dbc.Button(
                        [html.I(className="fas fa-check-circle", style={'marginRight': '8px'}), "Sélectionner les filtres"],
                        id='select-filters-button',
                        color="danger",
                        style=sidebar_styles['button_primary'],
                        className="w-100 mt-3"
                    ),
                ]),
            ], id='filter-selection-panel'),
            
            # Configuration des filtres (initialement masqué)
            html.Div([
                html.Div([
                    html.I(className="fas fa-search", style={'marginRight': '8px', 'color': sfr_colors['red']}),
                    "Configuration des filtres"
                ], style=sidebar_styles['section_title']),
                
                # Affichage du nombre d'observations actuelles
                html.Div(id="filter-stats", style={'marginBottom': '15px'}),
                
                # Container pour les filtres configurables (généré dynamiquement)
                html.Div(id="filter-config-container"),
                
                # Bouton pour réinitialiser tous les filtres
                html.Div([
                    dbc.Button(
                        [html.I(className="fas fa-sync-alt", style={'marginRight': '8px'}), "Réinitialiser tous les filtres"],
                        id='reset-all-filters',
                        color="light",
                        style=sidebar_styles['button_secondary'],
                        className="w-100 mt-3"
                    ),
                ]),
                
                # Bouton pour revenir à la sélection des filtres
                html.Div([
                    dbc.Button(
                        [html.I(className="fas fa-arrow-left", style={'marginRight': '8px'}), "Modifier les catégories"],
                        id='back-to-selection',
                        color="light",
                        style=sidebar_styles['button_secondary'],
                        className="w-100 mt-3"
                    ),
                ]),
            ], id='filter-config-panel', style={'display': 'none'}),
            
        ], style=sidebar_styles['content']),
        
    ], style=sidebar_styles['container'])

def create_filter_component(filter_name, filter_options=None):
    """
    Crée un composant de filtre dynamique en fonction du type de filtre
    Args:
        filter_name: Nom du filtre à créer
        filter_options: Options disponibles pour ce filtre (peut être None)
    
    Returns:
        Un composant Dash pour ce filtre spécifique
    """
    # Correction de l'erreur d'échappement dans la f-string
    filter_id = f"filter-{filter_name.lower().replace(' ', '-').replace(chr(39), '')}"
    
    # Container pour le filtre avec titre
    filter_container = html.Div([
        html.Label(filter_name, style=sidebar_styles['label']),
    ], style=sidebar_styles['filter_section'])
    
    # Obtenir les options du gestionnaire de données
    data_manager = DataManager.get_instance()
    if filter_options is None:
        filter_options = data_manager.get_filter_options(filter_name)
    
    # Configurer le composant en fonction du type de filtre
    if filter_name == "Date":
        # Composant de sélection de dates
        filter_container.children.append(
            dcc.DatePickerRange(
                id={'type': 'filter-component', 'name': filter_name},
                start_date_placeholder_text="Date début",
                end_date_placeholder_text="Date fin",
                style=sidebar_styles['date_picker']
            )
        )
    elif filter_name == "Heure":
        # Slider pour sélectionner une plage horaire
        min_hour, max_hour = 0, 23
        if isinstance(filter_options, list) and len(filter_options) == 2:
            min_hour, max_hour = filter_options
            
        filter_container.children.append(
            dcc.RangeSlider(
                id={'type': 'filter-component', 'name': filter_name},
                min=min_hour,
                max=max_hour,
                step=1,
                marks={i: f"{i}h" for i in range(int(min_hour), int(max_hour)+1, 2)},
                value=[min_hour, max_hour]
            )
        )
    elif filter_name == "Jour de la semaine":
        # Checklist pour les jours de la semaine
        filter_container.children.append(
            dcc.Checklist(
                id={'type': 'filter-component', 'name': filter_name},
                options=[
                    {'label': 'Lundi', 'value': 0},
                    {'label': 'Mardi', 'value': 1},
                    {'label': 'Mercredi', 'value': 2},
                    {'label': 'Jeudi', 'value': 3},
                    {'label': 'Vendredi', 'value': 4},
                    {'label': 'Samedi', 'value': 5},
                    {'label': 'Dimanche', 'value': 6}
                ],
                value=[],
                style=sidebar_styles['checklist']
            )
        )
    elif filter_name in ["Week-end", "Heure de nuit", "Heure ouvrée", "Jour férié", 
                        "Heure de pointe", "Nouvelle boucle", "DSP 1", "DEP_PEAG_OLT_match"]:
        # Boutons radio pour les filtres booléens
        filter_container.children.append(
            dcc.RadioItems(
                id={'type': 'filter-component', 'name': filter_name},
                options=[
                    {'label': 'Tous', 'value': 'all'},
                    {'label': 'Oui', 'value': 'oui'},
                    {'label': 'Non', 'value': 'non'}
                ],
                value='all',
                style=sidebar_styles['radio_items']
            )
        )
    elif filter_name == "Nombre de clients":
        # Slider pour les valeurs numériques
        min_val, max_val = 0, 1000
        if isinstance(filter_options, list) and len(filter_options) == 2:
            min_val, max_val = filter_options
            
        filter_container.children.append(
            dcc.RangeSlider(
                id={'type': 'filter-component', 'name': filter_name},
                min=min_val,
                max=max_val,
                step=(max_val - min_val) / 100,  # Pas adaptatif
                marks={i: str(i) for i in range(int(min_val), int(max_val)+1, int((max_val - min_val)/5))},
                value=[min_val, max_val]
            )
        )
    else:
        # Par défaut, utiliser un dropdown
        placeholder_options = [{"label": "Chargement...", "value": ""}]
        if isinstance(filter_options, list) and filter_options:
            display_options = [{"label": opt, "value": opt} for opt in filter_options]
        else:
            display_options = placeholder_options
            
        # Ajouter un champ de recherche si les options sont nombreuses
        if len(display_options) > 10:
            filter_container.children.append(
                dcc.Input(
                    id={'type': 'filter-search', 'name': filter_name},
                    type='text',
                    placeholder=f"Rechercher dans {filter_name}...",
                    style=sidebar_styles['search_input']
                )
            )
            
        filter_container.children.append(
            dcc.Dropdown(
                id={'type': 'filter-component', 'name': filter_name},
                options=display_options,
                placeholder=f"Sélectionner {filter_name}...",
                style=sidebar_styles['dropdown']
            )
        )
    
    # Bouton d'application du filtre
    filter_container.children.append(
        html.Div([
            dbc.Button(
                "Appliquer",
                id={'type': 'apply-filter', 'name': filter_name},
                color="danger",
                size="sm",
                style=sidebar_styles['apply_button']
            )
        ], style={'textAlign': 'right', 'marginTop': '8px'})
    )
    
    return filter_container