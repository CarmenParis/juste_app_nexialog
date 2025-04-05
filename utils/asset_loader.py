# utils/asset_loader.py
import base64
import os
from dash import html
from styles.theme import sfr_colors

def load_sfr_logo(size='large'):
    """
    Charge le logo SFR à partir du fichier image.
    Args:
        size: 'large' ou 'small' pour différentes tailles de logo
    Returns:
        Composant html.Img contenant le logo
    """
    try:
        # Chemin absolu vers le fichier SFR.png au niveau de app.py
        # Nous remontons de deux niveaux depuis utils/asset_loader.py pour atteindre le niveau de app.py
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        image_filename = os.path.join(base_dir, 'SFR.png')
        
        # Lire et encoder l'image
        with open(image_filename, 'rb') as f:
            encoded_image = base64.b64encode(f.read()).decode('ascii')
        
        # Définir la taille selon le paramètre
        if size == 'large':
            return html.Img(src=f'data:image/png;base64,{encoded_image}', 
                           style={'height': '40px', 'marginRight': '15px'})
        elif size == 'small':
            return html.Img(src=f'data:image/png;base64,{encoded_image}', 
                           style={'height': '22px', 'marginRight': '10px', 'verticalAlign': 'middle'})
    except Exception as e:
        print(f"Erreur lors du chargement du logo: {e}")
        # Fallback si l'image n'est pas trouvée
        if size == 'large':
            return html.Div("SFR", style={'fontWeight': 'bold', 'fontSize': '24px', 'color': sfr_colors['red']})
        elif size == 'small':
            return html.Div("SFR", style={'fontWeight': 'bold', 'fontSize': '18px', 'color': sfr_colors['red']})