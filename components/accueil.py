# components/accueil.py
# Composant de la page d'accueil

from dash import html
import dash_bootstrap_components as dbc
from styles.theme import accueil_styles, sfr_colors

def create_accueil_layout():
    """
    Crée la mise en page de la page d'accueil avec un message de bienvenue
    et les photos des 4 acteurs du site
    Returns:
        Composant html.Div contenant la page d'accueil
    """
    return html.Div([
        # En-tête de bienvenue
        dbc.Container([
            # Section de bienvenue - Seulement le titre, pas de sous-texte
            html.Div([
                html.H1([
                    html.Span("Bienvenue sur ", style={"color": sfr_colors['dark_grey']}),
                    html.Span("S", style={"color": sfr_colors['red']}),
                    html.Span("peed", style={"color": sfr_colors['dark_grey']}),
                    html.Span("F", style={"color": sfr_colors['red']}),
                    html.Span("low", style={"color": sfr_colors['dark_grey']}),
                    html.Span("R", style={"color": sfr_colors['red']}),
                    html.Span("eliability", style={"color": sfr_colors['dark_grey']})
                ], style=accueil_styles["welcome_title"])
                # Suppression des deux lignes de texte en dessous du titre
            ], style=accueil_styles["welcome_header"]),
            
            # Section des acteurs du site
            html.Div([
                html.H2("Qui sommes-nous ?", style=accueil_styles["section_title"]),
                
                # Conteneur pour les 4 photos des acteurs
                html.Div([

                    # Nhi
                    html.Div([
                        html.Img(src="/assets/Nhi.png", style=accueil_styles["actor_photo_without_border"]),
                        html.H4("Nhi", style=accueil_styles["actor_name"])
                    ], style=accueil_styles["actor_card"]),
                    # Carmen
                    html.Div([
                        html.Img(src="/assets/Carmen.png", style=accueil_styles["actor_photo_without_border"]),
                        html.H4("Carmen", style=accueil_styles["actor_name"])
                    ], style=accueil_styles["actor_card"]),
                    
                    # Alisa
                    html.Div([
                        html.Img(src="/assets/Alisa.png", style=accueil_styles["actor_photo_without_border"]),
                        html.H4("Alisa", style=accueil_styles["actor_name"])
                    ], style=accueil_styles["actor_card"]),
                    
                    
                    # Lia
                    html.Div([
                        html.Img(src="/assets/Lia.png", style=accueil_styles["actor_photo_without_border"]),
                        html.H4("Lia", style=accueil_styles["actor_name"])
                    ], style=accueil_styles["actor_card"]),
                ], style=accueil_styles["actors_container"]),
            ], style=accueil_styles["team_section"]),
            
            # Section des fonctionnalités principales
            html.Div([
                html.H2("Fonctionnalités principales", style=accueil_styles["section_title"]),
                
                html.Div([
                    # Fonctionnalité 1
                    html.Div([
                        html.I(className="fas fa-chart-line", style=accueil_styles["feature_icon"]),
                        html.H3("Analyse de données", style=accueil_styles["feature_title"]),
                        html.P("Visualisez et analysez vos données DNS et réseau en temps réel.", style=accueil_styles["feature_desc"])
                    ], style=accueil_styles["feature_card"]),
                    
                    # Fonctionnalité 2
                    html.Div([
                        html.I(className="fas fa-filter", style=accueil_styles["feature_icon"]),
                        html.H3("Filtres personnalisés", style=accueil_styles["feature_title"]),
                        html.P("Filtrez vos données selon différents critères pour affiner votre analyse.", style=accueil_styles["feature_desc"])
                    ], style=accueil_styles["feature_card"]),
                    
                    # Fonctionnalité 3
                    html.Div([
                        html.I(className="fas fa-robot", style=accueil_styles["feature_icon"]),
                        html.H3("Assistant virtuel", style=accueil_styles["feature_title"]),
                        html.P("Interagissez avec notre assistant intelligent pour analyser vos données.", style=accueil_styles["feature_desc"])
                    ], style=accueil_styles["feature_card"]),
                ], style=accueil_styles["features_container"])
            ], style=accueil_styles["features_section"]),
            
        ], fluid=True)
    ], style=accueil_styles["accueil_container"])