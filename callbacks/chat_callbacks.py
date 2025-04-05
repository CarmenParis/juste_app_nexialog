# callbacks/chat_callbacks.py - Simplifié pour ne gérer que les messages texte
from dash import Input, Output, State, callback, html, ctx
from datetime import datetime

@callback(
    [Output("chat-messages", "children"),
     Output("chat-input-field", "value"),
     Output("filter-mode-active", "data")],
    [Input("chat-send-button", "n_clicks")],
    [State("chat-input-field", "value"),
     State("chat-messages", "children")],
    prevent_initial_call=True
)
def update_chat(send_clicks, message_text, chat_messages):
    """Gère les interactions du chat"""
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
        'color': '#404040',
        'boxShadow': '0 1px 2px rgba(0,0,0,0.07)',
    }
    
    # Style pour la bulle de l'utilisateur
    user_bubble_style = chat_bubble_style.copy()
    user_bubble_style.update({
        'float': 'right',
        'clear': 'both',
        'marginLeft': 'auto',
        'marginRight': '0',
    })
    
    # Style pour la bulle de l'assistant
    assistant_bubble_style = chat_bubble_style.copy()
    assistant_bubble_style.update({
        'float': 'left',
        'clear': 'both',
    })

    current_time = datetime.now().strftime("%H:%M")
    
    # Message texte envoyé par l'utilisateur
    if message_text:
        # Message utilisateur
        user_message = html.Div([
            html.Div(message_text,
                    style=user_bubble_style),
            html.Small(current_time, style={
                "fontSize": "10px", 
                "color": "#888", 
                "display": "block",
                "textAlign": "right",
                "clear": "both"
            })
        ])
        
        # Réponse de l'assistant
        assistant_message = html.Div([
            html.Div("Pour explorer les données en détail, utilisez les filtres disponibles dans la barre latérale à gauche.",
                    style=assistant_bubble_style),
            html.Small(current_time, style={"fontSize": "10px", "color": "#888", "clear": "both", "display": "block"})
        ])
        
        # Mettre à jour le chat
        updated_chat = chat_messages + [user_message, assistant_message]
        
        return updated_chat, "", False
    
    # Cas par défaut
    return chat_messages, "", False