# styles/theme.py
# Définition des couleurs et styles de l'application

# Couleurs SFR avec un fond doux
sfr_colors = {
    'red': '#e2001a',
    'dark_grey': '#404040',
    'medium_grey': '#777777',
    'light_grey': '#f5f5f5',
    'very_light_grey': '#fafafa',
    'white': '#ffffff',
    'background': '#f8f7f3',  # Couleur d'arrière-plan douce beige/crème
    'paper': '#fcfbf8',       # Couleur légèrement plus claire pour les éléments
}

# Styles avancés pour le composant chat
chat_styles = {
    'container': {
        'width': '100%',
        'border': '1px solid rgba(200, 200, 200, 0.5)',
        'borderRadius': '12px',
        'overflow': 'hidden',
        'marginTop': '0',
        'boxShadow': '0 8px 20px rgba(0,0,0,0.08)',
        'height': 'calc(100vh - 120px)',
        'display': 'flex',
        'flexDirection': 'column',
        'backgroundColor': sfr_colors['white'],
        'transition': 'all 0.3s ease',
        'fontFamily': '"Roboto", sans-serif',
    },
    'header': {
        'background': 'linear-gradient(90deg, #404040 0%, #505050 100%)',
        'color': sfr_colors['white'],
        'padding': '14px 18px',
        'fontWeight': '500',
        'fontSize': '16px',
        'display': 'flex',
        'alignItems': 'center',
        'boxShadow': '0 2px 4px rgba(0,0,0,0.08)',
    },
    'messages': {
        'flex': '1',
        'overflowY': 'auto',
        'padding': '25px',
        'background': sfr_colors['paper'],
        'scrollBehavior': 'smooth',
    },
    'input_container': {
        'display': 'flex',
        'padding': '15px',
        'borderTop': '1px solid rgba(220, 220, 220, 0.7)',
        'backgroundColor': sfr_colors['white'],
        'boxShadow': '0 -2px 10px rgba(0,0,0,0.02)',
    },
    'input': {
        'flex': '1',
        'padding': '12px 18px 12px 45px', # Espace pour l'icône
        'border': '1px solid rgba(190, 190, 190, 0.4)',
        'borderRadius': '24px',
        'fontSize': '14px',
        'marginRight': '12px',
        'transition': 'all 0.2s ease',
        'boxShadow': '0 1px 3px rgba(0,0,0,0.03)',
        'background': 'url("https://cdn-icons-png.flaticon.com/128/134/134914.png") no-repeat 15px center / 20px',
    },
    'button': {
        'backgroundColor': sfr_colors['red'],
        'color': sfr_colors['white'],
        'border': 'none',
        'padding': '10px 22px',
        'borderRadius': '24px',
        'cursor': 'pointer',
        'fontSize': '14px',
        'fontWeight': '500',
        'display': 'flex',
        'alignItems': 'center',
        'justifyContent': 'center',
        'transition': 'background-color 0.2s ease, transform 0.1s ease',
        'boxShadow': '0 2px 6px rgba(226, 0, 26, 0.3)',
    },
    'assistant_message': {
        'textAlign': 'left',
        'margin': '10px 0',
        'padding': '14px 20px',
        'backgroundColor': 'rgba(245, 245, 245, 0.9)',
        'color': sfr_colors['dark_grey'],
        'borderRadius': '20px 20px 20px 4px',
        'display': 'inline-block',
        'maxWidth': '80%',
        'wordWrap': 'break-word',
        'float': 'left',
        'clear': 'both',
        'boxShadow': '0 1px 2px rgba(0,0,0,0.07)',
        'fontSize': '15px',
        'lineHeight': '1.5',
    },
    'options_container': {
        'display': 'flex',
        'flexDirection': 'column',
        'gap': '10px',
        'margin': '15px 0',
        'clear': 'both',
    },
    'option_button': {
        'backgroundColor': 'rgba(255, 255, 255, 0.95)',
        'border': '1px solid rgba(190, 190, 190, 0.4)',
        'color': sfr_colors['dark_grey'],
        'borderRadius': '20px',
        'padding': '10px 18px 10px 45px',  # Espace pour l'icône
        'margin': '5px 0',
        'cursor': 'pointer',
        'textAlign': 'left',
        'transition': 'all 0.2s ease',
        'maxWidth': '90%',
        'alignSelf': 'flex-start',
        'fontSize': '14px',
        'position': 'relative',
        'boxShadow': '0 1px 3px rgba(0,0,0,0.03)',
    },
}

# Styles pour la barre latérale
sidebar_styles = {
    'container': {
        'height': 'calc(100vh - 120px)',
        'backgroundColor': sfr_colors['white'],
        'borderRadius': '12px',
        'boxShadow': '0 8px 20px rgba(0,0,0,0.08)',
        'overflow': 'hidden',
        'display': 'flex',
        'flexDirection': 'column',
        'transition': 'all 0.3s ease',
        'fontFamily': '"Roboto", sans-serif',
        'border': '1px solid rgba(200, 200, 200, 0.5)',
    },
    'header': {
        'background': 'linear-gradient(90deg, #404040 0%, #505050 100%)',
        'color': sfr_colors['white'],
        'padding': '14px 18px',
        'fontWeight': '500',
        'fontSize': '16px',
        'display': 'flex',
        'alignItems': 'center',
        'boxShadow': '0 2px 4px rgba(0,0,0,0.08)',
    },
    'content': {
        'flex': '1',
        'overflowY': 'auto',
        'padding': '20px',
        'background': sfr_colors['paper'],
    },
    'section_title': {
        'fontSize': '13px',
        'fontWeight': '500',
        'color': sfr_colors['dark_grey'],
        'marginBottom': '16px',
        'display': 'flex',
        'alignItems': 'center',
        'borderBottom': f'2px solid {sfr_colors["light_grey"]}',
        'paddingBottom': '8px',
    },
    'filter_section': {
        'marginBottom': '22px',
    },
    'label': {
        'display': 'block',
        'fontSize': '14px',
        'color': sfr_colors['dark_grey'],
        'marginBottom': '8px',
        'fontWeight': '500',
    },
    'dropdown': {
        'width': '100%',
        'border': '1px solid rgba(190, 190, 190, 0.4)',
        'borderRadius': '6px',
        'boxShadow': '0 1px 3px rgba(0,0,0,0.03)',
    },
    'date_picker': {
        'width': '100%',
        'zIndex': '100',
    },
    'checklist': {
        'fontSize': '14px',
        'color': sfr_colors['dark_grey'],
        'marginBottom': '10px',
    },
    'radio_items': {
        'fontSize': '14px',
        'color': sfr_colors['dark_grey'],
        'marginBottom': '10px',
    },
    'search_input': {
        'width': '100%',
        'padding': '8px 12px',
        'border': '1px solid rgba(190, 190, 190, 0.4)',
        'borderRadius': '6px',
        'fontSize': '14px',
        'marginBottom': '8px',
        'boxShadow': '0 1px 3px rgba(0,0,0,0.03)',
    },
    'button_primary': {
        'backgroundColor': sfr_colors['red'],
        'color': sfr_colors['white'],
        'border': 'none',
        'padding': '8px 16px',
        'fontSize': '14px',
        'fontWeight': '500',
        'borderRadius': '6px',
        'boxShadow': '0 2px 6px rgba(226, 0, 26, 0.3)',
    },
    'button_secondary': {
        'backgroundColor': sfr_colors['light_grey'],
        'color': sfr_colors['dark_grey'],
        'border': 'none',
        'padding': '8px 16px',
        'fontSize': '14px',
        'fontWeight': '500',
        'borderRadius': '6px',
    },
    'action_buttons': {
        'display': 'flex',
        'justifyContent': 'space-between',
        'marginTop': '10px',
    },
    'apply_button': {
        'backgroundColor': sfr_colors['red'],
        'color': sfr_colors['white'],
        'border': 'none',
        'padding': '5px 12px',
        'fontSize': '13px',
        'fontWeight': '500',
        'borderRadius': '4px',
        'boxShadow': '0 1px 3px rgba(226, 0, 26, 0.3)',
    }
}

# Style pour la navbar
navbar_styles = {
    'navbar': {
        'background': 'linear-gradient(90deg, #404040 0%, #505050 100%)',
        'boxShadow': '0 2px 8px rgba(0,0,0,0.15)',
        'padding': '12px 20px',
    },
    'title_container': {
        'display': 'flex',
        'flexDirection': 'column',
        'alignItems': 'flex-start',
        'marginLeft': '15px'
    },
    'title': {
        'fontSize': '18px',
        'fontWeight': '500',
        'margin': '0',
        'padding': '0',
        'color': sfr_colors['white'],
        'fontFamily': '"Roboto", sans-serif',
    },
    'subtitle': {
        'fontSize': '12px',
        'color': 'rgba(255, 255, 255, 0.85)',
        'margin': '2px 0 0 0',
        'padding': '0',
        'fontFamily': '"Roboto", sans-serif',
    },
    'nav_link': {
        'color': 'rgba(255, 255, 255, 0.85)',
        'fontWeight': '400',
        'padding': '8px 15px',
        'borderRadius': '4px',
    }
}

# Styles pour la page d'accueil
accueil_styles = {
    "accueil_container": {
        'fontFamily': 'Roboto, sans-serif',
        'backgroundColor': sfr_colors['background'],
        'minHeight': 'calc(100vh - 56px)',
        'padding': '30px 0'
    },
    "welcome_header": {
        'backgroundColor': sfr_colors['white'],
        'padding': '40px',
        'borderRadius': '12px',
        'boxShadow': '0 2px 10px rgba(0, 0, 0, 0.1)',
        'textAlign': 'center',
        'marginBottom': '40px'  # Augmenté pour compenser la suppression des sous-textes
    },
    "welcome_title": {
        'fontFamily': 'Roboto, sans-serif',
        'fontWeight': '700',
        'marginBottom': '0',  # Pas de marge en bas puisqu'il n'y a plus de texte dessous
        'fontSize': '2rem', # Légèrement plus grand
        'textAlign': 'center'
        # Pas de couleur définie ici car nous utilisons des spans avec des couleurs différentes
    },
    "welcome_subtitle": {
        'color': sfr_colors['dark_grey'],
        'fontWeight': '400',
        'marginBottom': '20px',
        'fontSize': '1.5rem'
    },
    "welcome_text": {
        'color': sfr_colors['medium_grey'],
        'fontSize': '1.1rem',
        'maxWidth': '800px',
        'margin': '0 auto'
    },
    "section_title": {
    'textAlign': 'center',
    'color': sfr_colors['dark_grey'],
    'marginBottom': '30px',  # Même valeur que welcome_title
    'marginTop': '70px',
    'fontSize': '1.8rem',
    'fontWeight': '700',  # Même valeur que welcome_title (gras)
    'fontFamily': 'Roboto, sans-serif'
    },
    "team_section": {
        'marginBottom': '50px'
    },
    "actors_container": {
        'display': 'flex',
        'justifyContent': 'center',
        'flexWrap': 'wrap',
        'gap': '25px'
    },
    "actor_card": {
        'width': '220px',
        'textAlign': 'center',
        'padding': '20px',
        'backgroundColor': sfr_colors['white'],
        'borderRadius': '12px',
        'boxShadow': '0 2px 8px rgba(0, 0, 0, 0.1)',
        'transition': 'transform 0.3s ease'
    },
    "actor_photo": {
        'width': '150px',
        'height': '150px',
        'borderRadius': '50%',
        'objectFit': 'cover',
        'marginBottom': '15px',
        'border': f'3px solid {sfr_colors["red"]}'
    },
    "actor_photo_without_border": {
        'width': '150px',
        'height': '150px',
        'borderRadius': '50%',
        'objectFit': 'cover',
        'marginBottom': '15px'
    },
    "actor_name": {
        'color': sfr_colors['dark_grey'],
        'marginBottom': '5px',
        'fontSize': '1.2rem',
        'fontWeight': '500',
        'fontFamily': 'Roboto, sans-serif'  # Uniformiser la police
    },
    "actor_role": {
        'color': sfr_colors['medium_grey'],
        'fontSize': '0.9rem'
    },
    "features_section": {
        'backgroundColor': sfr_colors['white'],
        'padding': '40px',
        'borderRadius': '12px',
        'boxShadow': '0 2px 10px rgba(0, 0, 0, 0.1)'
    },
    "features_container": {
        'display': 'flex',
        'justifyContent': 'center',
        'flexWrap': 'wrap',
        'gap': '30px'
    },
    "feature_card": {
        'width': '300px',
        'padding': '25px',
        'backgroundColor': sfr_colors['very_light_grey'],
        'borderRadius': '12px',
        'boxShadow': '0 2px 8px rgba(0, 0, 0, 0.05)',
        'textAlign': 'center'
    },
    "feature_icon": {
        'fontSize': '2.5rem',
        'color': sfr_colors['red'],
        'marginBottom': '15px'
    },
    "feature_title": {
        'color': sfr_colors['dark_grey'],
        'marginBottom': '10px',
        'fontSize': '1.3rem',
        'fontWeight': '500',
        'fontFamily': 'Roboto, sans-serif'  # Uniformiser la police
    },
    "feature_desc": {
        'color': sfr_colors['medium_grey'],
        'fontSize': '0.95rem',
        'fontFamily': 'Roboto, sans-serif'  # Uniformiser la police
    }
}

# Style pour le contenu principal
main_content_style = {
    'background': sfr_colors['background'],
    'minHeight': 'calc(100vh - 65px)',
    'padding': '0'
}

# CSS personnalisé pour le HTML
custom_css = '''
<style>
    body {
        font-family: 'Roboto', sans-serif;
        margin: 0;
        padding: 0;
        background-color: #f8f7f3;
    }
    input:focus {
        border-color: #e2001a !important;
        box-shadow: 0 0 0 3px rgba(226, 0, 26, 0.1) !important;
        outline: none !important;
    }
    button:hover {
        background-color: #c50017 !important;
    }
    [style*="option_button"]:hover {
        background-color: #f0f0f0 !important;
        border-color: #c0c0c0 !important;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1) !important;
    }
    .sidebar-column {
        padding-right: 15px;
    }
    .chat-column {
        padding-left: 15px;
    }
    /* Styles pour les dropdowns et les datepickers */
    .Select-control:hover {
        border-color: rgba(226, 0, 26, 0.5) !important;
    }
    .Select.is-focused > .Select-control {
        border-color: #e2001a !important;
        box-shadow: 0 0 0 3px rgba(226, 0, 26, 0.1) !important;
    }
    .SingleDatePickerInput, .DateRangePickerInput {
        border-color: rgba(190, 190, 190, 0.4) !important;
        border-radius: 6px !important;
    }
    .SingleDatePickerInput:hover, .DateRangePickerInput:hover {
        border-color: rgba(226, 0, 26, 0.5) !important;
    }
    .CalendarDay--selected, .CalendarDay--selected:hover {
        background: #e2001a !important;
        border: 1px double #e2001a !important;
    }
    /* Styles pour les checklist et radio buttons */
    .radio-group label, .checkbox-group label {
        display: flex;
        align-items: center;
        margin-bottom: 5px;
    }
    .radio-group input, .checkbox-group input {
        margin-right: 8px;
    }
    /* Style pour le scrollbar de la sidebar */
    .sidebar-content::-webkit-scrollbar {
        width: 8px;
    }
    .sidebar-content::-webkit-scrollbar-track {
        background: #f1f1f1;
        border-radius: 4px;
    }
    .sidebar-content::-webkit-scrollbar-thumb {
        background: #ddd;
        border-radius: 4px;
    }
    .sidebar-content::-webkit-scrollbar-thumb:hover {
        background: #ccc;
    }
    /* Styles pour la page d'accueil */
    .actor-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1) !important;
    }
    .feature-card:hover {
        background-color: #f0f0f0 !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08) !important;
    }
    .feature-icon {
        transition: transform 0.3s ease;
    }
    .feature-card:hover .feature-icon {
        transform: scale(1.1);
    }
</style>
'''

# Styles pour la page de modélisation
modelisation_styles = {
    "modelisation_container": {
        "padding": "20px 0",
        "backgroundColor": "#f9f9f9",
        "minHeight": "100vh"
    },
    "header": {
        "textAlign": "center",
        "padding": "30px 0",
        "marginBottom": "20px"
    },
    "page_title": {
        "fontSize": "2.5rem",
        "fontWeight": "bold",
        "marginBottom": "10px"
    },
    "description_container": {
        "textAlign": "center",
        "marginBottom": "40px"
    },
    "description": {
        "fontSize": "1.2rem",
        "color": sfr_colors['dark_grey']
    },
    "models_container": {
        "display": "flex",
        "flexWrap": "wrap",
        "justifyContent": "center",
        "gap": "30px"
    },
    "model_card": {
        "width": "270px",
        "backgroundColor": sfr_colors['white'],
        "borderRadius": "10px",
        "overflow": "hidden",
        "boxShadow": "0 4px 8px rgba(0, 0, 0, 0.1)",
        "transition": "transform 0.3s ease, box-shadow 0.3s ease",
        ":hover": {
            "transform": "translateY(-5px)",
            "boxShadow": "0 8px 16px rgba(0, 0, 0, 0.2)"
        }
    },
    "model_link": {
        "textDecoration": "none",
        "color": "inherit",
        "display": "block",
        "height": "100%"
    },
    "model_content": {
        "padding": "25px",
        "textAlign": "center"
    },
    "model_icon": {
        "fontSize": "3rem",
        "color": sfr_colors['red'],
        "marginBottom": "15px"
    },
    "model_title": {
        "fontSize": "1.5rem",
        "color": sfr_colors['dark_grey'],
        "marginBottom": "15px"
    },
    "model_desc": {
        "color": sfr_colors['dark_grey'],
        "fontSize": "0.9rem"
    }
}

