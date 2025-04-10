# components/modelisation.py
# Composant pour la page de modélisation

from dash import html, dcc
import dash_bootstrap_components as dbc
from styles.theme import sfr_colors, modelisation_styles

def create_modelisation_layout():
    """
    Crée la mise en page de la page de modélisation avec des boxes cliquables
    Returns:
        Composant html.Div contenant la page de modélisation
    """
    return html.Div([
        dbc.Container([
            # En-tête de la page
            html.Div([
                html.H1([
                    html.Span("M", style={"color": sfr_colors['red']}),
                    html.Span("Modélisation", style={"color": sfr_colors['dark_grey']})
                ], style=modelisation_styles["page_title"])
            ], style=modelisation_styles["header"]),
            
            # Description de la page
            html.Div([
                html.P("Sélectionnez un modèle pour visualiser ses résultats et ses performances.", 
                       style=modelisation_styles["description"])
            ], style=modelisation_styles["description_container"]),
            
            # Conteneur pour les boxes de modèles
            html.Div([
                # Modèle 1
                html.Div([
                    html.A([
                        html.Div([
                            html.I(className="fas fa-chart-line", style=modelisation_styles["model_icon"]),
                            html.H3("Modèle de Carmen", style=modelisation_styles["model_title"]),
                            html.P("Info modele", 
                                   style=modelisation_styles["model_desc"])
                        ], style=modelisation_styles["model_content"])
                    ], href="/modelisation/carmen", style=modelisation_styles["model_link"])
                ], style=modelisation_styles["model_card"]),
                
                # Modèle 2
                html.Div([
                    html.A([
                        html.Div([
                            html.I(className="fas fa-network-wired", style=modelisation_styles["model_icon"]),
                            html.H3("Isolation Forest", style=modelisation_styles["model_title"]),
                            html.P("Détecter les anomalies de OLT", 
                                   style=modelisation_styles["model_desc"])
                        ], style=modelisation_styles["model_content"])
                    ], href="/modelisation/nhi", style=modelisation_styles["model_link"])
                ], style=modelisation_styles["model_card"]),
                
                # Modèle 3
                html.Div([
                    html.A([
                        html.Div([
                            html.I(className="fas fa-tree", style=modelisation_styles["model_icon"]),
                            html.H3("Modele de Lia", style=modelisation_styles["model_title"]),
                            html.P("Info modele", 
                                   style=modelisation_styles["model_desc"])
                        ], style=modelisation_styles["model_content"])
                    ], href="/modelisation/Lia", style=modelisation_styles["model_link"])
                ], style=modelisation_styles["model_card"]),
                
                # Modèle 4
                html.Div([
                    html.A([
                        html.Div([
                            html.I(className="fas fa-project-diagram", style=modelisation_styles["model_icon"]),
                            html.H3("Modele de Alisa", style=modelisation_styles["model_title"]),
                            html.P("Info modele", 
                                   style=modelisation_styles["model_desc"])
                        ], style=modelisation_styles["model_content"])
                    ], href="/modelisation/Alisa", style=modelisation_styles["model_link"])
                ], style=modelisation_styles["model_card"]),
            ], style=modelisation_styles["models_container"]),
            
        ], fluid=True)
    ], style=modelisation_styles["modelisation_container"])