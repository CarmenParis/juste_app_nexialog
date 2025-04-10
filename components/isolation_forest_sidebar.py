# components/isolation_forest_sidebar.py
# Composant de barre latérale spécifique pour la page de détection des anomalies

import dash
from dash import html, dcc, callback, Input, Output, State, ALL, MATCH, no_update
import dash_bootstrap_components as dbc
from styles.theme import sidebar_styles, sfr_colors
from utils.data_loader import DataManager
from datetime import datetime, timedelta

def create_isolation_forest_sidebar():
    """
    Crée une barre latérale simplifiée avec les filtres jour, heure et contamination
    pour la page de détection des anomalies avec Isolation Forest
    
    Returns:
        Composant html.Div contenant la barre latérale simplifiée
    """
    # Définir les plages de dates pour le calendrier
    start_date = datetime(2024, 12, 1)
    end_date = datetime(2025, 1, 31)
    
    # Date par défaut (aujourd'hui ou la date la plus récente disponible)
    default_date = min(datetime.now().date(), end_date.date())
    default_date = max(default_date, start_date.date())  # S'assurer que la date est dans la plage autorisée
    
    return html.Div([
        # En-tête de la barre latérale
        html.Div([
            html.I(className="fas fa-filter", style={'marginRight': '10px', 'color': sfr_colors['red']}),
            "Filtres d'anomalies"
        ], style=sidebar_styles['header']),
        
        # Store pour les valeurs des filtres configurés
        dcc.Store(id='isolation-forest-filter-values', data={}),
        
        # Contenu de la barre latérale
        html.Div([
            html.Div([
                html.I(className="fas fa-search", style={'marginRight': '8px', 'color': sfr_colors['red']}),
                "Configuration des filtres"
            ], style=sidebar_styles['section_title']),
            
            # Filtre OLT (olt_name)
            html.Div([
                html.Label("OLT", style=sidebar_styles['label']),
                # Champ de recherche pour les OLT
                dcc.Input(
                    id='olt-search',
                    type='text',
                    placeholder="Rechercher un OLT...",
                    style=sidebar_styles['search_input']
                ),
                # Dropdown pour sélectionner l'OLT
                dcc.Dropdown(
                    id='olt-filter',
                    placeholder="Sélectionner un OLT...",
                    style=sidebar_styles['dropdown'],
                    clearable=True
                ),
            ], style=sidebar_styles['filter_section']),
            
            # Calendrier pour sélectionner une plage de dates
            html.Div([
                html.Label("Période", style=sidebar_styles['label']),
                # Date Picker Range pour sélectionner la période
                dcc.DatePickerRange(
                    id='date-range-filter',
                    min_date_allowed=start_date,
                    max_date_allowed=end_date,
                    initial_visible_month=datetime(2025, 1, 1),
                    start_date=default_date,
                    end_date=default_date,
                    display_format='DD/MM/YYYY',
                    first_day_of_week=1,  # Lundi comme premier jour de la semaine
                    stay_open_on_select=False,
                    with_portal=True,  # Ouvre le calendrier dans un portail pour mieux l'afficher
                    style=sidebar_styles['date_picker'] if 'date_picker' in sidebar_styles else {'width': '100%'}
                ),
                html.Div(id="date-range-output", style={'textAlign': 'center', 'marginTop': '8px', 'fontSize': '12px'})
            ], style=sidebar_styles['filter_section']),
            
            # Filtre Time (hour)
            html.Div([
                html.Label("Plage horaire", style=sidebar_styles['label']),
                # Slider pour sélectionner une plage horaire
                dcc.RangeSlider(
                    id='hour-filter',
                    min=0,
                    max=23,
                    step=1,
                    marks={i: f"{i}h" for i in range(0, 24, 2)},
                    value=[1, 23]  # Valeur par défaut 1h-23h comme dans l'image
                ),
                # Affichage des valeurs sélectionnées
                html.Div(id="hour-filter-output", style={'textAlign': 'center', 'marginTop': '8px'}),
            ], style=sidebar_styles['filter_section']),
            
            # Section Statistiques d'anomalies avec filtre de contamination
            html.Div([
                html.Label("Statistiques d'anomalies", style=sidebar_styles['label']),
                html.Div([
                    html.Label("Niveau de contamination:", style={'marginBottom': '5px', 'fontSize': '14px'}),
                    dbc.ButtonGroup(
                        [
                            dbc.Button("0.001", id="contamination-0001", color="outline-primary", size="sm", 
                                      className="mr-1", n_clicks=0, active=False),
                            dbc.Button("0.005", id="contamination-0005", color="outline-primary", size="sm", 
                                      className="mr-1", n_clicks=0, active=True),
                            dbc.Button("0.01", id="contamination-001", color="outline-primary", size="sm", 
                                      n_clicks=0, active=False)
                        ],
                        style={'width': '100%', 'marginBottom': '15px'}
                    ),
                    dcc.Store(id='current-contamination', data=0.005),  # Valeur par défaut
                    html.P([
                        html.Small("La contamination représente la proportion attendue d'anomalies dans les données. Une valeur plus petite détecte moins d'anomalies mais avec plus de précision.", 
                               style={'color': sfr_colors['dark_grey'], 'fontStyle': 'italic'})
                    ], style={'marginTop': '5px'})
                ], style={'marginTop': '10px'})
            ], style=sidebar_styles['filter_section']),
            
            # Bouton pour appliquer les filtres
            html.Div([
                dbc.Button(
                    [html.I(className="fas fa-check-circle", style={'marginRight': '8px'}), "Appliquer les filtres"],
                    id='apply-anomaly-filters',
                    color="danger",
                    style=sidebar_styles['button_primary'],
                    className="w-100 mt-3"
                ),
            ]),
            
            # Bouton pour réinitialiser tous les filtres
            html.Div([
                dbc.Button(
                    [html.I(className="fas fa-sync-alt", style={'marginRight': '8px'}), "Réinitialiser les filtres"],
                    id='reset-anomaly-filters',
                    color="light",
                    style=sidebar_styles['button_secondary'],
                    className="w-100 mt-3"
                ),
            ]),
        ], style=sidebar_styles['content']),
        
    ], style=sidebar_styles['container'])

# Fonction pour les callbacks
def init_isolation_forest_sidebar_callbacks(app):
    """
    Initialise les callbacks pour la barre latérale de détection des anomalies
    
    Args:
        app: Instance de l'application Dash
    """
    
    # Callback pour mettre à jour l'affichage de la plage horaire sélectionnée
    @app.callback(
        Output("hour-filter-output", "children"),
        Input("hour-filter", "value")
    )
    def update_hour_output(value):
        if not value:
            return ""
        return f"Plage sélectionnée : {value[0]}h - {value[1]}h"
    
    # Callback pour l'affichage de la plage de dates sélectionnée
    @app.callback(
        Output("date-range-output", "children"),
        [Input("date-range-filter", "start_date"),
         Input("date-range-filter", "end_date")]
    )
    def update_date_range_output(start_date, end_date):
        if not start_date or not end_date:
            return ""
            
        # Convertir les dates en objets datetime
        start = datetime.strptime(start_date.split('T')[0], "%Y-%m-%d")
        end = datetime.strptime(end_date.split('T')[0], "%Y-%m-%d")
        
        # Formater les dates pour l'affichage
        start_str = start.strftime("%d/%m/%Y")
        end_str = end.strftime("%d/%m/%Y")
        
        # Calculer le nombre de jours
        days = (end - start).days + 1
        day_text = "jour" if days == 1 else "jours"
        
        return f"Période: {start_str} à {end_str} ({days} {day_text})"
    
    # Callback pour filtrer les options de l'OLT en fonction de la recherche
    @app.callback(
        Output("olt-filter", "options"),
        Input("olt-search", "value")
    )
    def filter_olts(search_term):
        # Ici, vous devriez charger la liste complète des OLTs depuis votre source de données
        data_manager = DataManager.get_instance()
        all_olts = data_manager.get_filter_options("Identifiant d'OLT")  # Adapter selon votre implémentation
        
        if not search_term:
            return [{"label": olt, "value": olt} for olt in all_olts]
        
        # Filtrer les OLTs qui contiennent le terme de recherche
        filtered_olts = [olt for olt in all_olts if search_term and search_term.lower() in olt.lower()]
        return [{"label": olt, "value": olt} for olt in filtered_olts]
    
    # Callbacks pour gérer les boutons de contamination et mettre à jour les filtres automatiquement
    @app.callback(
        [Output("contamination-0001", "active"),
         Output("contamination-0005", "active"),
         Output("contamination-001", "active"),
         Output("current-contamination", "data"),
         Output("isolation-forest-filter-values", "data")],  # Nouvelle sortie
        [Input("contamination-0001", "n_clicks"),
         Input("contamination-0005", "n_clicks"),
         Input("contamination-001", "n_clicks")],
        [State("olt-filter", "value"),
         State("date-range-filter", "start_date"),
         State("date-range-filter", "end_date"),
         State("hour-filter", "value"),
         State("isolation-forest-filter-values", "data")]  # Nouveaux états
    )
    def update_contamination_selection(clicks_0001, clicks_0005, clicks_001, 
                                      olt_value, start_date, end_date, hour_value, current_filters):
        ctx = dash.callback_context
        if not ctx.triggered:
            # Par défaut, 0.005 est sélectionné
            return False, True, False, 0.005, dash.no_update
        
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]
        
        # Déterminer la nouvelle valeur de contamination
        if button_id == "contamination-0001":
            new_contamination = 0.001
            active_states = (True, False, False)
        elif button_id == "contamination-0005":
            new_contamination = 0.005
            active_states = (False, True, False)
        elif button_id == "contamination-001":
            new_contamination = 0.01
            active_states = (False, False, True)
        else:
            new_contamination = 0.005
            active_states = (False, True, False)
        
        # Mettre à jour les filtres comme dans apply_filters
        if current_filters is None:
            current_filters = {}
        
        # Convertir les dates au format approprié
        date_range = []
        if start_date and end_date:
            start = datetime.strptime(start_date.split('T')[0], "%Y-%m-%d")
            end = datetime.strptime(end_date.split('T')[0], "%Y-%m-%d")
            
            # Générer toutes les dates dans la plage
            current_date = start
            while current_date <= end:
                date_range.append(current_date.strftime("%Y-%m-%d"))
                current_date += timedelta(days=1)
        
        # Préserver les valeurs actuelles des filtres et mettre à jour la contamination
        current_filters.update({
            "olt_name": olt_value,
            "start_date": start_date.split('T')[0] if start_date else None,
            "end_date": end_date.split('T')[0] if end_date else None,
            "date_range": date_range,
            "hour": hour_value,
            "contamination": new_contamination
        })
        
        return (*active_states, new_contamination, current_filters)
    
    # Callback pour appliquer les filtres
    @app.callback(
        Output("isolation-forest-filter-values", "data", allow_duplicate=True),  # Ajout de allow_duplicate
        Input("apply-anomaly-filters", "n_clicks"),
        [State("olt-filter", "value"),
         State("date-range-filter", "start_date"),
         State("date-range-filter", "end_date"),
         State("hour-filter", "value"),
         State("current-contamination", "data"),
         State("isolation-forest-filter-values", "data")],
        prevent_initial_call=True
    )
    def apply_filters(n_clicks, olt_value, start_date, end_date, hour_value, contamination, current_filters):
        if n_clicks is None:
            return dash.no_update
        
        # Convertir les dates au format approprié
        date_range = []
        if start_date and end_date:
            start = datetime.strptime(start_date.split('T')[0], "%Y-%m-%d")
            end = datetime.strptime(end_date.split('T')[0], "%Y-%m-%d")
            
            # Générer toutes les dates dans la plage
            current_date = start
            while current_date <= end:
                date_range.append(current_date.strftime("%Y-%m-%d"))
                current_date += timedelta(days=1)
        
        # Mettre à jour les filtres
        if current_filters is None:
            current_filters = {}
            
        current_filters.update({
            "olt_name": olt_value,
            "start_date": start_date.split('T')[0] if start_date else None,
            "end_date": end_date.split('T')[0] if end_date else None,
            "date_range": date_range,
            "hour": hour_value,
            "contamination": contamination
        })
        
        return current_filters
    
    # Callback pour réinitialiser les filtres
    @app.callback(
        [Output("olt-filter", "value"),
         Output("date-range-filter", "start_date"),
         Output("date-range-filter", "end_date"),
         Output("hour-filter", "value")],
        Input("reset-anomaly-filters", "n_clicks"),
        prevent_initial_call=True
    )
    def reset_filters(n_clicks):
        today = datetime.now().date()
        today_str = today.strftime("%Y-%m-%d")
        return None, today_str, today_str, [0, 23]
