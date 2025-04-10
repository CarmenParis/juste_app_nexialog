# components/alisa_lof_sidebar.py
import dash
from dash import html, dcc, callback, Input, Output, State
import dash_bootstrap_components as dbc
from styles.theme import sidebar_styles, sfr_colors
from datetime import datetime, timedelta
import pandas as pd
import os

def create_alisa_lof_sidebar():
    """
    Crée une barre latérale pour le modèle LOF avec des filtres personnalisés
    """
    # Construire le chemin du fichier CSV
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    csv_path = os.path.join(base_dir, 'lof.csv')
    
    # Valeurs par défaut
    min_date = datetime.now().date()
    max_date = datetime.now().date()
    default_date = datetime.now().date()
    unique_chains = ['Toutes']
    
    # Essayer de charger le fichier CSV
    try:
        df_detected = pd.read_csv(csv_path, low_memory=False)
        
        # Créer un timestamp si nécessaire
        if 'timestamp' not in df_detected.columns:
            # Vérifier les colonnes disponibles pour créer le timestamp
            if 'jour' in df_detected.columns and 'heure' in df_detected.columns:
                df_detected['timestamp'] = pd.to_datetime(
                    df_detected['jour'] + ' ' + 
                    df_detected['heure'].astype(str) + ':00:00'
                )
            else:
                raise ValueError("Impossible de créer un timestamp")
        
        # Créer la colonne chaine_id si elle n'existe pas
        if 'chaine_id' not in df_detected.columns:
            # Vérifier les colonnes nécessaires
            required_cols = ['code_departement', 'peag_nro', 'boucle_simplifiée', 'olt_name']
            if all(col in df_detected.columns for col in required_cols):
                df_detected['chaine_id'] = (
                    df_detected['code_departement'].astype(str) + '_' +
                    df_detected['peag_nro'] + '_' +
                    df_detected['boucle_simplifiée'] + '_' +
                    df_detected['olt_name']
                )
            else:
                raise ValueError("Colonnes requises pour créer chaine_id manquantes")
        
        # Définir les dates
        min_date = df_detected['timestamp'].min().date()
        max_date = df_detected['timestamp'].max().date()
        default_date = max_date
        
        # Récupérer les chaînes uniques
        unique_chains = ['Toutes'] + sorted(df_detected['chaine_id'].unique().tolist())
    
    except Exception as e:
        print(f"Erreur lors du chargement du fichier CSV: {e}")
    
    # Options pour les seuils LOF
    lof_thresholds = [
        {'label': '0.01 (stricte)', 'value': '001'},
        {'label': '0.03 (recommandé)', 'value': '003'},
        {'label': '0.05 (modéré)', 'value': '005'},
        {'label': '0.1 (permissif)', 'value': '01'}
    ]
    
    return html.Div([
        # En-tête de la barre latérale
        html.Div([
            html.I(className="fas fa-filter", style={'marginRight': '10px', 'color': sfr_colors['red']}),
            "Filtres LOF"
        ], style=sidebar_styles['header']),
        
        # Store pour les valeurs des filtres
        dcc.Store(id='lof-filter-values', data={}),
        
        # Contenu de la barre latérale
        html.Div([
            # Sélection de la date
            html.Div([
                html.Label("Date de référence", style=sidebar_styles['label']),
                dcc.DatePickerSingle(
                    id='lof-date-picker',
                    min_date_allowed=min_date,
                    max_date_allowed=max_date,
                    initial_visible_month=default_date,
                    date=default_date,
                    display_format='DD/MM/YYYY'
                )
            ], style=sidebar_styles['filter_section']),
            
            # Sélection de l'heure
            html.Div([
                html.Label("Heure", style=sidebar_styles['label']),
                dcc.Dropdown(
                    id='lof-hour-dropdown',
                    options=[{'label': f'{i}h00', 'value': i} for i in range(24)],
                    value=12,
                    clearable=False
                )
            ], style=sidebar_styles['filter_section']),
            
            # Sélection de la fenêtre temporelle
            html.Div([
                html.Label("Fenêtre temporelle", style=sidebar_styles['label']),
                dcc.RadioItems(
                    id='lof-timeframe-selection',
                    options=[
                        {'label': '1 heure', 'value': 1},
                        {'label': '3 heures', 'value': 3},
                        {'label': '7 heures', 'value': 7},
                        {'label': '12 heures', 'value': 12},
                        {'label': '24 heures', 'value': 24}
                    ],
                    value=3,
                    inline=True,
                    className="mb-3"
                )
            ], style=sidebar_styles['filter_section']),
            
            # Sélection du seuil LOF
            html.Div([
                html.Label("Seuil LOF", style=sidebar_styles['label']),
                dcc.RadioItems(
                    id='lof-threshold-selection',
                    options=lof_thresholds,
                    value='003',
                    inline=True,
                    className="mb-3"
                )
            ], style=sidebar_styles['filter_section']),
            
            # Filtrage par chaîne
            html.Div([
                html.Label("Filtrer par chaîne", style=sidebar_styles['label']),
                dcc.Dropdown(
                    id='lof-chain-filter',
                    options=[{'label': chain, 'value': chain} for chain in unique_chains],
                    value='Toutes',
                    clearable=False
                )
            ], style=sidebar_styles['filter_section']),
            
            # Filtrage par indicateur
            html.Div([
                html.Label("Filtrer par indicateur", style=sidebar_styles['label']),
                dcc.Dropdown(
                    id='lof-indicator-filter',
                    options=[
                        {'label': 'Tous', 'value': 'all'},
                        {'label': 'DNS', 'value': 'dns'},
                        {'label': 'Score', 'value': 'score'},
                        {'label': 'Latence', 'value': 'latency'}
                    ],
                    value='all',
                    clearable=False
                )
            ], style=sidebar_styles['filter_section']),
            
            # Boutons d'action
            html.Div([
                dbc.Button(
                    [html.I(className="fas fa-check-circle", style={'marginRight': '8px'}), "Appliquer"],
                    id='apply-lof-filters',
                    color="danger",
                    style=sidebar_styles['button_primary'],
                    className="w-100 mt-3"
                ),
                dbc.Button(
                    [html.I(className="fas fa-sync-alt", style={'marginRight': '8px'}), "Réinitialiser"],
                    id='reset-lof-filters',
                    color="light",
                    style=sidebar_styles['button_secondary'],
                    className="w-100 mt-3"
                )
            ])
        ], style=sidebar_styles['content'])
    ], style=sidebar_styles['container'])

# Callbacks pour la sidebar
def init_alisa_lof_sidebar_callbacks(app):
    @app.callback(
        Output('lof-filter-values', 'data'),
        [Input('apply-lof-filters', 'n_clicks')],
        [State('lof-date-picker', 'date'),
         State('lof-hour-dropdown', 'value'),
         State('lof-timeframe-selection', 'value'),
         State('lof-threshold-selection', 'value'),
         State('lof-chain-filter', 'value'),
         State('lof-indicator-filter', 'value')]
    )
    def update_lof_filters(n_clicks, date, hour, timeframe, lof_threshold, chain_filter, indicator_filter):
        if n_clicks is None:
            return {}
        
        return {
            'date': date,
            'hour': hour,
            'timeframe': timeframe,
            'lof_threshold': lof_threshold,
            'chain_filter': chain_filter,
            'indicator_filter': indicator_filter
        }
    
    @app.callback(
        [Output('lof-date-picker', 'date'),
         Output('lof-hour-dropdown', 'value'),
         Output('lof-timeframe-selection', 'value'),
         Output('lof-threshold-selection', 'value'),
         Output('lof-chain-filter', 'value'),
         Output('lof-indicator-filter', 'value')],
        Input('reset-lof-filters', 'n_clicks'),
        prevent_initial_call=True
    )
    def reset_lof_filters(n_clicks):
        # Valeurs par défaut
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        csv_path = os.path.join(base_dir, 'lof.csv')
        
        try:
            df_detected = pd.read_csv(csv_path)
            
            # Créer un timestamp si nécessaire
            if 'timestamp' not in df_detected.columns:
                df_detected['timestamp'] = pd.to_datetime(
                    df_detected['jour'] + ' ' + 
                    df_detected['heure'].astype(str) + ':00:00'
                )
            
            default_date = df_detected['timestamp'].max().date()
        except Exception:
            default_date = datetime.now().date()
        
        return (default_date, 12, 3, '003', 'Toutes', 'all')

    return app