# utils/auto_scroll.py
from dash import callback, Input, Output, State, html, ctx

def auto_scroll_callback():
    """
    Enregistre un callback pour faire défiler automatiquement la zone de chat 
    vers le bas lorsque de nouveaux messages sont ajoutés
    """
    @callback(
        Output("chat-messages", "style", allow_duplicate=True),
        Input("chat-messages", "children"),
        State("chat-messages", "style"),
        prevent_initial_call=True
    )
    def scroll_to_bottom(children, current_style):
        if not current_style:
            current_style = {}
        
        # On clone le style actuel et on ajoute scrollBehavior: 'smooth'
        updated_style = current_style.copy()
        updated_style.update({
            'scrollBehavior': 'smooth',
            'scrollMarginBottom': '100px'  # Ajoute une marge pour éviter que le dernier message ne soit caché
        })
        
        # On utilise javascript pour faire défiler vers le bas
        return updated_style
        
    return None