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

# Importer les callbacks (doit être fait après la définition du layout)
from callbacks import chat_callbacks, sidebar_callbacks

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