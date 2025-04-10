# app.py
# Point d'entrée principal de l'application

import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output

# Importer nos composants
from components.navbar import create_navbar, init_navbar_callbacks
from components.chat import create_chat_component
from components.sidebar import create_sidebar
from components.accueil import create_accueil_layout
# Importer le composant de modélisation
from components.modelisation import create_modelisation_layout
# Importer la nouvelle sidebar pour Isolation Forest
from components.isolation_forest_sidebar import create_isolation_forest_sidebar, init_isolation_forest_sidebar_callbacks
from styles.theme import main_content_style, custom_css

# Initialiser l'application
app = dash.Dash(__name__,
                external_stylesheets=[
                    dbc.themes.BOOTSTRAP,
                    "https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&display=swap",
                    "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css"
                ],
                suppress_callback_exceptions=True)

# Layout principal avec support pour différentes pages
app.layout = html.Div([
    # Store l'URL actuelle
    dcc.Location(id='url', refresh=False),
    
    # Barre de navigation (sera mise à jour dynamiquement)
    create_navbar(),
    
    # Contenu de la page qui changera en fonction de l'URL
    html.Div(id='page-content')
])

# Callback pour changer le contenu en fonction de l'URL
@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    print(f"URL actuelle: {pathname}")  # Ajout pour le débogage
    
    # Page d'accueil
    if pathname == '/accueil' or pathname == '/':
        return create_accueil_layout()
    
    # Page assistant (layout original)
    elif pathname == '/assistant':
        return html.Div([
            dbc.Container([
                dbc.Row([
                    # Barre latérale à gauche
                    dbc.Col(create_sidebar(), width=3, className="sidebar-column"),
                    
                    # Chat à droite
                    dbc.Col(create_chat_component(), width=9, className="chat-column")
                ], className="pt-4")  # Padding top
            ], fluid=True)
        ], style=main_content_style)
    
    # Page d'aide
    elif pathname == '/aide':
        return html.Div([
            dbc.Container([
                html.H1("Aide et Documentation", className="my-4"),
                html.P("Cette page est en cours de construction. Elle contiendra bientôt une documentation complète sur l'utilisation d'ESEFIRIUS.")
            ], fluid=True)
        ], style=main_content_style)
    
    # Page de modélisation
    elif pathname == '/modelisation' or pathname.startswith('/modelisation/'):
        # Page principale de modélisation
        if pathname == '/modelisation':
            return create_modelisation_layout()
        # Sous-pages de modélisation selon les modèles définis dans le composant
        elif pathname == '/modelisation/carmen':
            return html.Div([
                dbc.Container([
                    html.H1("Modèle de Carmen", className="my-4"),
                    html.P("Cette page affichera les résultats du modèle de Carmen."),
                    html.A("Retour aux modèles", href="/modelisation", className="btn btn-outline-primary mt-3")
                ], fluid=True)
            ], style=main_content_style)
        elif pathname.lower() == '/modelisation/nhi':  # Utiliser .lower() pour rendre la comparaison insensible à la casse
            # Layout spécifique pour la page de détection d'anomalies avec Isolation Forest
            return html.Div([
                dbc.Container([
                    dbc.Row([
                        # Barre latérale spécifique à gauche
                        dbc.Col(create_isolation_forest_sidebar(), width=3, className="sidebar-column"),
                        
                        # Contenu à droite
                        dbc.Col([
                            html.H1("Détection des anomalies avec Isolation Forest", className="my-4"),
                            
                            # Div pour explication
                            html.Div([
                                html.H4("Description du modèle"),
                                html.P("""
                                    L'algorithme Isolation Forest est utilisé pour détecter des anomalies dans 
                                    les données de trafic réseau. Il fonctionne en isolant les observations qui 
                                    s'écartent significativement du comportement normal du réseau. Le paramètre
                                    de contamination permet de définir la proportion attendue d'anomalies dans 
                                    les données.
                                """, className="mb-4"),
                            ], className="mb-4 p-3 border rounded"),
                            
                            # Conteneur pour les graphiques (sera rempli dynamiquement)
                            html.Div([
                                dcc.Loading(
                                    id="loading-anomalies",
                                    type="circle",
                                    children=[
                                        html.Div(id="anomaly-visualization-container")
                                    ]
                                )
                            ], className="mt-4"),
                            
                            # Bouton pour revenir à la page de modélisation
                            html.A("Retour aux modèles", href="/modelisation", className="btn btn-outline-primary mt-3 mb-4")
                        ], width=9, className="content-column")
                    ], className="pt-4")  # Padding top
                ], fluid=True)
            ], style=main_content_style)
        elif pathname.lower() == '/modelisation/alisa':
            return html.Div([
                dbc.Container([
                    html.H1("Modèle de Alisa", className="my-4"),
                    html.P("Cette page affichera les résultats du modèle de Alisa."),
                    html.A("Retour aux modèles", href="/modelisation", className="btn btn-outline-primary mt-3")
                ], fluid=True)
            ], style=main_content_style)
        elif pathname.lower() == '/modelisation/lia':
            return html.Div([
                dbc.Container([
                    html.H1("Modèle de Lia", className="my-4"),
                    html.P("Cette page affichera les résultats du modèle de Lia."),
                    html.A("Retour aux modèles", href="/modelisation", className="btn btn-outline-primary mt-3")
                ], fluid=True)
            ], style=main_content_style)
        else:
            # Redirection vers la page principale de modélisation si l'URL n'est pas valide
            return create_modelisation_layout()
    
    # Redirection par défaut vers la page d'accueil
    else:
        return create_accueil_layout()

# CSS personnalisé
app.index_string = f'''
<!DOCTYPE html>
<html>
    <head>
        {{%metas%}}
        <title>ESEFIRIUS - Assistant virtuel SFR</title>
        {{%favicon%}}
        {{%css%}}
        {custom_css}
    </head>
    <body>
        {{%app_entry%}}
        <footer>
            {{%config%}}
            {{%scripts%}}
            {{%renderer%}}
        </footer>
    </body>
</html>
'''

# Initialiser les callbacks de la navbar
init_navbar_callbacks(app)

# Initialiser les callbacks pour la sidebar d'Isolation Forest
init_isolation_forest_sidebar_callbacks(app)

# Importer les callbacks (doit être fait après la définition du layout)
from callbacks import chat_callbacks, sidebar_callbacks

# Importer les callbacks pour la page de détection d'anomalies
from callbacks.isolation_forest_callbacks import init_isolation_forest_callbacks
init_isolation_forest_callbacks(app)

# Auto-scroll callback
from dash import clientside_callback

# Cette fonction crée un callback côté client pour faire défiler automatiquement la conversation vers le bas
clientside_callback(
    """
    function(children) {
        const chatContainer = document.getElementById('chat-messages');
        if (chatContainer) {
            setTimeout(function() {
                chatContainer.scrollTop = chatContainer.scrollHeight;
            }, 100);
        }
        return window.dash_clientside.no_update;
    }
    """,
    Output("chat-messages", "data-scroll", allow_duplicate=True),
    Input("chat-messages", "children"),
    prevent_initial_call=True
)

# Lancer l'application
if __name__ == '__main__':
    app.run(debug=True)
