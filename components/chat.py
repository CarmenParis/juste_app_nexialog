# components/chat.py
from dash import html, dcc
from datetime import datetime
import base64
import os
import pandas as pd
from utils.data_loader import DataManager

def create_chat_component():
    """Crée le composant de chat complet"""
    # Date et heure actuelles
    current_time = datetime.now().strftime("%H:%M")
    
    # Obtenir le gestionnaire de données pour accéder aux statistiques
    data_manager = DataManager.get_instance()
    
    # Couleurs
    colors = {
        'beige': '#f8f7f3',      # Couleur de fond principale beige
        'dark_grey': '#404040',  # Gris foncé pour l'en-tête
        'red': '#e2001a',        # Rouge SFR
        'light_grey': '#f0f0f0'  # Gris clair pour les messages
    }
    
    # Style uniforme pour les bulles de chat
    chat_bubble_style = {
        'backgroundColor': '#f0f0f0',  # Gris léger uniforme
        'padding': '12px 16px',
        'borderRadius': '12px',
        'display': 'inline-block',
        'maxWidth': '80%',
        'marginBottom': '8px',
        'fontSize': '14px',
        'lineHeight': '1.5',
        'color': colors['dark_grey'],
        'boxShadow': '0 1px 2px rgba(0,0,0,0.07)',
    }
    
    # Charger l'image directement depuis le fichier
    try:
        # Chemin vers le fichier SFR.png au niveau de app.py
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        image_path = os.path.join(base_dir, 'SFR.png')
        
        # Encoder l'image en base64
        with open(image_path, 'rb') as f:
            encoded_image = base64.b64encode(f.read()).decode('ascii')
            
        # Créer la source de l'image
        img_src = f'data:image/png;base64,{encoded_image}'
    except Exception as e:
        print(f"Erreur lors du chargement du logo: {e}")
        img_src = ""  # Image vide en cas d'erreur
    
    # Préparer les statistiques générales
    try:
        nb_observations = len(data_manager.df)
        nb_olts = data_manager.df['olt_name'].nunique()
        nb_peags = data_manager.df['peag_nro'].nunique()
        nb_departements = data_manager.df['code_departement'].nunique()
        nb_pop_dns = data_manager.df['pop_dns'].nunique()
        nb_boucles = data_manager.df['boucle'].nunique()
        nb_pebibs = data_manager.df['pebib'].nunique()
        
        # Formatage des dates min et max
        dates = pd.to_datetime(data_manager.df['date'])
        min_date = dates.min().strftime('%d/%m/%Y')
        max_date = dates.max().strftime('%d/%m/%Y')
        periode = f"{min_date} - {max_date}"
    except Exception as e:
        print(f"Erreur lors du calcul des statistiques: {e}")
        # Valeurs par défaut en cas d'erreur
        nb_observations = "-"
        nb_olts = "-"
        nb_peags = "-" 
        nb_departements = "-"
        nb_pop_dns = "-"
        nb_boucles = "-"
        nb_pebibs = "-"
        periode = "-"
        
    
    # Formater les nombres avec espace comme séparateur de milliers
    def format_number(num):
        if isinstance(num, (int, float)):
            return f"{num:,}".replace(',', ' ')
        return str(num)
    
    return html.Div([
        # En-tête du chat
        html.Div([
            #html.Img(src=img_src, height="30px"),
            html.Span("Assistant ESEFIRIUS", style={"marginLeft": "10px"})
        ], style={
            "background": colors['dark_grey'],
            "color": "white",
            "padding": "15px",
            "borderRadius": "10px 10px 0 0",
            "display": "flex",
            "alignItems": "center"
        }),
        
        # Zone des messages
        html.Div([
            # Message de bienvenue avec instructions intégrées
            html.Div([
                html.Div([
                    html.P("Je suis votre assistant ESEFIRIUS. Je vais vous accompagner dans l'exploration et l'analyse de vos données."),
                    html.P("ESEFIRIUS vous permet de :"),
                    html.Ul([
                        html.Li("Explorer vos données via différents filtres personnalisables"),
                        html.Li("Visualiser des statistiques sur le réseau SFR"),
                        html.Li("Analyser les performances par région, équipement, période, etc.")
                    ])
                ], style=chat_bubble_style),
                html.Small(current_time, style={"color": "#888", "fontSize": "10px"})
            ], style={"marginBottom": "20px"}),
            
            # Statistiques générales intégrées directement dans le chat
            html.Div([
                html.Div([
                    html.P("Voici les statistiques générales du réseau :", 
                           style={"fontWeight": "bold", "marginBottom": "10px"}),
                    html.Div([
                        # Ligne 1 de cartes
                        html.Div([
                            # Carte 1: Nombre d'observations
                            html.Div([
                                html.I(className="fas fa-database", style={'fontSize': '24px', 'color': colors['red'], 'marginBottom': '8px'}),
                                html.Div("Observations", style={'fontWeight': 'bold', 'marginBottom': '5px'}),
                                html.Div(format_number(nb_observations), style={'fontSize': '16px'})
                            ], style={'padding': '12px', 'backgroundColor': 'white', 'borderRadius': '8px', 'textAlign': 'center',
                                     'boxShadow': '0 2px 5px rgba(0,0,0,0.1)', 'flex': '1', 'margin': '5px', 'minWidth': '110px'}),
                            
                            # Carte 2: Période couverte
                            html.Div([
                                html.I(className="fas fa-calendar-alt", style={'fontSize': '24px', 'color': colors['red'], 'marginBottom': '8px'}),
                                html.Div("Période", style={'fontWeight': 'bold', 'marginBottom': '5px'}),
                                html.Div(periode, style={'fontSize': '16px'})
                            ], style={'padding': '12px', 'backgroundColor': 'white', 'borderRadius': '8px', 'textAlign': 'center',
                                     'boxShadow': '0 2px 5px rgba(0,0,0,0.1)', 'flex': '1', 'margin': '5px', 'minWidth': '110px'}),
                            
                            # Carte 3: Nombre de départements
                            html.Div([
                                html.I(className="fas fa-map-marker-alt", style={'fontSize': '24px', 'color': colors['red'], 'marginBottom': '8px'}),
                                html.Div("Départements", style={'fontWeight': 'bold', 'marginBottom': '5px'}),
                                html.Div(format_number(nb_departements), style={'fontSize': '16px'})
                            ], style={'padding': '12px', 'backgroundColor': 'white', 'borderRadius': '8px', 'textAlign': 'center',
                                     'boxShadow': '0 2px 5px rgba(0,0,0,0.1)', 'flex': '1', 'margin': '5px', 'minWidth': '110px'})
                        ], style={'display': 'flex', 'flexWrap': 'wrap', 'gap': '5px', 'marginBottom': '10px', 'justifyContent': 'center'}),
                        
                        # Ligne 2 de cartes
                        html.Div([
                            # Carte 4: Nombre de boucles
                            html.Div([
                                html.I(className="fas fa-circle-notch", style={'fontSize': '24px', 'color': colors['red'], 'marginBottom': '8px'}),
                                html.Div("Boucles", style={'fontWeight': 'bold', 'marginBottom': '5px'}),
                                html.Div(format_number(nb_boucles), style={'fontSize': '16px'})
                            ], style={'padding': '12px', 'backgroundColor': 'white', 'borderRadius': '8px', 'textAlign': 'center',
                                     'boxShadow': '0 2px 5px rgba(0,0,0,0.1)', 'flex': '1', 'margin': '5px', 'minWidth': '110px'}),
                            
                            # Carte 5: Nombre de PEAGs
                            html.Div([
                                html.I(className="fas fa-server", style={'fontSize': '24px', 'color': colors['red'], 'marginBottom': '8px'}),
                                html.Div("PEAGs", style={'fontWeight': 'bold', 'marginBottom': '5px'}),
                                html.Div(format_number(nb_peags), style={'fontSize': '16px'})
                            ], style={'padding': '12px', 'backgroundColor': 'white', 'borderRadius': '8px', 'textAlign': 'center',
                                     'boxShadow': '0 2px 5px rgba(0,0,0,0.1)', 'flex': '1', 'margin': '5px', 'minWidth': '110px'}),
                            
                            # Carte 6: Nombre d'OLTs
                            html.Div([
                                html.I(className="fas fa-network-wired", style={'fontSize': '24px', 'color': colors['red'], 'marginBottom': '8px'}),
                                html.Div("OLTs", style={'fontWeight': 'bold', 'marginBottom': '5px'}),
                                html.Div(format_number(nb_olts), style={'fontSize': '16px'})
                            ], style={'padding': '12px', 'backgroundColor': 'white', 'borderRadius': '8px', 'textAlign': 'center',
                                     'boxShadow': '0 2px 5px rgba(0,0,0,0.1)', 'flex': '1', 'margin': '5px', 'minWidth': '110px'})
                        ], style={'display': 'flex', 'flexWrap': 'wrap', 'gap': '5px', 'marginBottom': '10px', 'justifyContent': 'center'}),
                        
                        # Ligne 3 de cartes
                        html.Div([
                            # Carte 7: Nombre de PEBIBs
                            html.Div([
                                html.I(className="fas fa-hdd", style={'fontSize': '24px', 'color': colors['red'], 'marginBottom': '8px'}),
                                html.Div("PEBIBs", style={'fontWeight': 'bold', 'marginBottom': '5px'}),
                                html.Div(format_number(nb_pebibs), style={'fontSize': '16px'})
                            ], style={'padding': '12px', 'backgroundColor': 'white', 'borderRadius': '8px', 'textAlign': 'center',
                                     'boxShadow': '0 2px 5px rgba(0,0,0,0.1)', 'flex': '1', 'margin': '5px', 'minWidth': '110px'}),
                            
                            # Carte 8: POP DNS
                            html.Div([
                                html.I(className="fas fa-sitemap", style={'fontSize': '24px', 'color': colors['red'], 'marginBottom': '8px'}),
                                html.Div("POP DNS", style={'fontWeight': 'bold', 'marginBottom': '5px'}),
                                html.Div(format_number(nb_pop_dns), style={'fontSize': '16px'})
                            ], style={'padding': '12px', 'backgroundColor': 'white', 'borderRadius': '8px', 'textAlign': 'center',
                                     'boxShadow': '0 2px 5px rgba(0,0,0,0.1)', 'flex': '1', 'margin': '5px', 'minWidth': '110px'})
                        ], style={'display': 'flex', 'flexWrap': 'wrap', 'gap': '5px', 'marginBottom': '10px', 'justifyContent': 'center'})
                    ]),
                    
                    html.P("Pour une analyse plus détaillée, utilisez les filtres dans la barre latérale de gauche.", 
                          style={"marginTop": "15px"})
                ], style=chat_bubble_style),
                html.Small(current_time, style={"color": "#888", "fontSize": "10px"})
            ], style={"marginBottom": "20px"})
            
            # Le bouton "Analyser avec filtres personnalisés" a été supprimé
            
        ], id="chat-messages",**{"data-scroll": ""},  style={
            "flex": "1",
            "overflowY": "auto",
            "padding": "20px",
            "backgroundColor": colors['beige']
        }),
        
        # Saisie de texte
        html.Div([
            dcc.Input(
                id="chat-input-field",
                type="text",
                placeholder="Entrez votre message...",
                style={
                    "width": "85%",
                    "padding": "10px 15px",
                    "borderRadius": "20px",
                    "border": "1px solid #ddd"
                }
            ),
            html.Button([
                html.I(className="fas fa-paper-plane")
            ], id="chat-send-button", style={
                "backgroundColor": colors['red'],
                "color": "white",
                "border": "none",
                "borderRadius": "50%",
                "width": "40px",
                "height": "40px",
                "marginLeft": "10px",
                "cursor": "pointer"
            })
        ], style={
            "padding": "15px",
            "borderTop": "1px solid #ddd",
            "display": "flex",
            "alignItems": "center",
            "backgroundColor": "white"
        }),
        
        # Store pour mode filtre
        dcc.Store(id="filter-mode-active", data=False)
    ], style={
        "border": "1px solid #ddd",
        "borderRadius": "10px",
        "backgroundColor": colors['beige'],
        "height": "calc(100vh - 120px)",
        "boxShadow": "0 0 15px rgba(0,0,0,0.1)",
        "display": "flex",
        "flexDirection": "column",
        "overflow": "hidden"
    })