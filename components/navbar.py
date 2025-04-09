# components/navbar.py
# Composant de barre de navigation dynamique

from dash import html, dcc
import dash_bootstrap_components as dbc
from styles.theme import navbar_styles
from utils.asset_loader import load_sfr_logo
from dash.dependencies import Input, Output

def create_navbar():
    """
    Crée la barre de navigation qui sera mise à jour dynamiquement
    Returns:
        Composant html.Div contenant la barre de navigation dynamique
    """
    return html.Div(id='navbar-content')

def create_navbar_content(pathname):
    """
    Crée le contenu de la barre de navigation en fonction de la page actuelle
    Args:
        pathname: Chemin de l'URL actuelle
    Returns:
        Composant html.Div contenant la barre de navigation avec le contenu approprié
    """
    sfr_logo = load_sfr_logo(size='large')
    
    # Déterminer le contenu de la navbar en fonction de la page
    if pathname == '/assistant':
        # Version pour la page EDA Assistant - conserve la navbar originale avec ESEFIRIUS
        return html.Div([
            dbc.Container([
                html.Div([
                    # Logo et titre
                    html.Div([
                        html.A(
                            sfr_logo,
                            href="/accueil",
                            style={"textDecoration": "none"}
                        ),
                        html.Div([
                            html.Div("Bienvenue sur ESEFIRIUS, votre assistant virtuel SFR", 
                                     style=navbar_styles['title']),
                            html.Div("Exploration et analyse de données grâce à des filtres personnalisés", 
                                     style=navbar_styles['subtitle'])
                        ], style=navbar_styles['title_container'])
                    ], style={'display': 'flex', 'alignItems': 'center'}),
                    
                    # Navigation
                    html.Div([
                        html.A("Page d'accueil", href="/accueil", 
                               style={'color': 'rgba(255, 255, 255, 0.8)', 'margin': '0 15px', 'textDecoration': 'none'}),
                        html.A("EDA Assistant", href="/assistant", 
                               style={'color': '#fff', 'margin': '0 15px', 'fontWeight': '500', 'textDecoration': 'none'}),
                        html.A("Aide", href="/aide", 
                               style={'color': 'rgba(255, 255, 255, 0.8)', 'margin': '0 15px', 'textDecoration': 'none'})
                    ], style={'display': 'flex', 'marginLeft': 'auto'})
                ], style={'display': 'flex', 'alignItems': 'center', 'justifyContent': 'space-between'})
            ], fluid=True)
        ], style=navbar_styles['navbar'])
    else:
        # Version pour la page d'accueil et autres pages - simplifiée sans texte, juste le logo
        return html.Div([
            dbc.Container([
                html.Div([
                    # Logo SFR seulement
                    html.A(
                        sfr_logo,
                        href="/accueil",
                        style={"textDecoration": "none"}
                    ),
                    
                    # Navigation à droite
                    html.Div([
                        html.A("Page d'accueil", href="/accueil", 
                               style={'color': 'rgba(255, 255, 255, 0.8)', 'margin': '0 15px', 'textDecoration': 'none'}),
                        html.A("EDA Assistant", href="/assistant", 
                               style={'color': '#fff', 'margin': '0 15px', 'fontWeight': '500', 'textDecoration': 'none'}),
                        html.A("Aide", href="/aide", 
                               style={'color': 'rgba(255, 255, 255, 0.8)', 'margin': '0 15px', 'textDecoration': 'none'})
                    ], style={'display': 'flex', 'marginLeft': 'auto'})
                ], style={'display': 'flex', 'alignItems': 'center', 'justifyContent': 'space-between'})
            ], fluid=True)
        ], style=navbar_styles['navbar'])

def init_navbar_callbacks(app):
    """
    Initialise les callbacks pour la barre de navigation dynamique
    Args:
        app: L'application Dash
    """
    @app.callback(
        Output('navbar-content', 'children'),
        [Input('url', 'pathname')]
    )
    def update_navbar(pathname):
        return create_navbar_content(pathname)