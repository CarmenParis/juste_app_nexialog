# callbacks/sidebar_callbacks.py
# Callbacks pour les interactions de la barre latérale

from dash import Input, Output, State, callback, html, dcc, ALL, MATCH, ctx, no_update
import dash_bootstrap_components as dbc
import pandas as pd
from datetime import datetime
from styles.theme import sfr_colors
from utils.data_loader import DataManager
import numpy as np
import plotly.express as px
# Importer les fonctions graphiques depuis le nouveau module
from utils.graph_utils import (
    create_structure_stats_graphs, 
    create_attributes_stats_graphs,
    create_temporal_stats_graphs,
    create_france_map_with_department
)
# Importer le callback de défilement automatique
from utils.auto_scroll import auto_scroll_callback

# Obtenir l'instance du gestionnaire de données
data_manager = DataManager.get_instance()

# Style uniforme pour les bulles de chat (côté utilisateur et assistant)
chat_bubble_style = {
    'backgroundColor': '#f0f0f0',  # Gris léger uniforme
    'padding': '12px 16px',
    'borderRadius': '12px',
    'display': 'inline-block',
    'maxWidth': '80%',
    'marginBottom': '8px',
    'fontSize': '14px',
    'lineHeight': '1.5',
    'color': sfr_colors['dark_grey'],
    'boxShadow': '0 1px 2px rgba(0,0,0,0.07)',
}

# Style pour la bulle de l'utilisateur (différence sur la position)
user_bubble_style = chat_bubble_style.copy()
user_bubble_style.update({
    'float': 'right',
    'clear': 'both',
    'marginLeft': 'auto',
    'marginRight': '0',
})

# Style pour la bulle de l'assistant (différence sur la position)
# Style pour la bulle de l'assistant (différence sur la position)
assistant_bubble_style = chat_bubble_style.copy()
assistant_bubble_style.update({
    'float': 'left',
    'clear': 'both',
    'maxWidth': '95%',  # Augmenter la largeur maximale
    'minWidth': '800px', # Largeur minimale pour contenir les graphiques
    'width': 'auto'      # Largeur automatique
})
# Style pour les boutons de statistiques
stats_button_style = {
    "backgroundColor": "#f0f0f0",
    "border": "1px solid #ddd",
    "borderRadius": "20px",
    "padding": "10px 15px",
    "margin": "5px 0",
    "width": "100%",
    "textAlign": "center",
    "cursor": "pointer",
    "transition": "all 0.2s ease",
    "boxShadow": "0 2px 4px rgba(0,0,0,0.05)",
    "color": "#404040",
    "fontSize": "14px"
}

def format_filter_selection(structure_filters, attributs_filters, temporels_filters):
    """
    Formate les filtres sélectionnés en une liste claire
    """
    all_filters = []
    
    # Ajouter les filtres techniques - Structure
    if structure_filters:
        all_filters.append(html.Div([
            html.Strong("Filtres techniques – Structure :"),
            html.Ul([html.Li(filter_name) for filter_name in structure_filters])
        ]))
    
    # Ajouter les filtres techniques - Attributs
    if attributs_filters:
        all_filters.append(html.Div([
            html.Strong("Filtres techniques – Attributs :"),
            html.Ul([html.Li(filter_name) for filter_name in attributs_filters])
        ]))
    
    # Ajouter les filtres temporels
    if temporels_filters:
        all_filters.append(html.Div([
            html.Strong("Filtres temporels :"),
            html.Ul([html.Li(filter_name) for filter_name in temporels_filters])
        ]))
    
    return html.Div(all_filters)

@callback(
    [Output('filter-selection-panel', 'style'),
     Output('filter-config-panel', 'style'),
     Output('selected-filter-categories', 'data'),
     Output('filter-config-container', 'children'),
     Output('chat-messages', 'children', allow_duplicate=True)],
    [Input('select-filters-button', 'n_clicks'),
     Input('back-to-selection', 'n_clicks')],
    [State('filtres-structure', 'value'),
     State('filtres-attributs', 'value'),
     State('filtres-temporels', 'value'),
     State('selected-filter-categories', 'data'),
     State('chat-messages', 'children')],
    prevent_initial_call=True
)
def toggle_filter_panels(select_clicks, back_clicks, structure_filters, attributs_filters, 
                         temporels_filters, selected_filters, chat_messages):
    """
    Gère la transition entre la phase de sélection et la phase de configuration
    """
    trigger_id = ctx.triggered_id
    
    # Cas 1: Passage de la sélection à la configuration
    if trigger_id == 'select-filters-button' and select_clicks:
        # Collecter tous les filtres sélectionnés
        all_filters = []
        if structure_filters:
            all_filters.extend(structure_filters)
        if attributs_filters:
            all_filters.extend(attributs_filters)
        if temporels_filters:
            all_filters.extend(temporels_filters)
        
        # Si aucun filtre n'est sélectionné, ne rien faire
        if not all_filters:
            return {'display': 'block'}, {'display': 'none'}, [], [], chat_messages
        
        # Créer les composants de filtres
        filter_components = []
        
        # Ajouter un indicateur d'état des filtres (uniquement pour les stats)
        filter_components.append(
            html.Div(
                id='filter-stats',
                children="",
                style={'marginBottom': '20px', 'padding': '10px', 'backgroundColor': sfr_colors['very_light_grey'], 'borderRadius': '5px', 'fontWeight': '500'}
            )
        )
        
        # Élément invisible pour stocker l'état des filtres (nécessaire pour callbacks)
        filter_components.append(
            html.Div(
                id='filter-status',
                style={'display': 'none'}
            )
        )
        
        # Ajouter les composants de filtre individuels
        for filter_name in all_filters:
            from components.sidebar import create_filter_component
            # Récupérer les options du filtre depuis le gestionnaire de données
            filter_options = data_manager.get_filter_options(filter_name)
            filter_components.append(create_filter_component(filter_name, filter_options))
        
        # Ajouter message au chat
        current_time = datetime.now().strftime("%H:%M")
        
        # Message utilisateur dans le chat
        user_message = html.Div([
            html.Div([
                html.P("J'ai sélectionné les filtres suivants :"),
                format_filter_selection(structure_filters, attributs_filters, temporels_filters)
            ],
            style=user_bubble_style),
            html.Small(current_time, 
                       style={'fontSize': '10px', 
                              'color': '#888', 
                              'marginTop': '5px', 
                              'display': 'block',
                              'textAlign': 'right',
                              'clear': 'both'})
        ])
        
        # Réponse de l'assistant dans le chat
        assistant_message = html.Div([
            html.Div([
                "Ces filtres sont bien pris en compte. Vous pouvez maintenant les configurer dans la section \"Configuration des filtres\".",
            ],
                    style=assistant_bubble_style),
            html.Small(current_time, 
                      style={'fontSize': '10px', 
                            'color': '#888', 
                            'marginTop': '5px', 
                            'display': 'block',
                            'clear': 'both'})
        ])
        
        # Mettre à jour le chat
        updated_chat = chat_messages + [user_message, assistant_message]
        
        return {'display': 'none'}, {'display': 'block'}, all_filters, filter_components, updated_chat
    
    # Cas 2: Retour à la sélection
    elif trigger_id == 'back-to-selection':
        return {'display': 'block'}, {'display': 'none'}, selected_filters, [], chat_messages
    
    # Par défaut, ne rien changer
    return {'display': 'block'}, {'display': 'none'}, [], [], chat_messages

@callback(
    [Output('filter-values', 'data'),
     Output('filter-stats', 'children'),
     Output('filter-status', 'children'),
     Output('chat-messages', 'children', allow_duplicate=True)],
    [Input({'type': 'apply-filter', 'name': ALL}, 'n_clicks')],  # Uniquement l'input du bouton Appliquer
    [State({'type': 'filter-component', 'name': ALL}, 'value'),
     State({'type': 'filter-component', 'name': ALL}, 'id'),
     State('filter-values', 'data'),
     State('chat-messages', 'children')],
    prevent_initial_call=True
)
def apply_filter(apply_clicks, filter_values, filter_ids, current_filters, chat_messages):
    """
    Applique un filtre spécifique uniquement lorsque le bouton Appliquer est cliqué
    """
    # Vérifier si le callback a bien été déclenché par un clic sur Appliquer
    trigger = ctx.triggered_id
    if not trigger or not any(apply_clicks):
        return current_filters, no_update, no_update, chat_messages
    
    filter_name = trigger['name']
    
    # Trouver l'index du filtre correspondant
    filter_index = None
    for i, filter_id in enumerate(filter_ids):
        if filter_id['name'] == filter_name:
            filter_index = i
            break
    
    if filter_index is None:
        return current_filters, no_update, no_update, chat_messages
    
    # Récupérer la valeur du filtre
    filter_value = filter_values[filter_index]
    
    # Mettre à jour les filtres
    updated_filters = current_filters.copy() if current_filters else {}
    updated_filters[filter_name] = filter_value
    
    # Obtenir le nombre de lignes après filtrage
    row_count = data_manager.get_filtered_row_count(updated_filters)
    
    # Créer le message de statistiques (uniquement nombre d'observations)
    stats_message = html.Div([
        html.I(className="fas fa-info-circle", style={'marginRight': '8px', 'color': sfr_colors['red']}),
        f"Nombre d'observations : {row_count:,}".replace(',', ' ')
    ], style={'backgroundColor': '#f0f0f0', 'padding': '10px', 'borderRadius': '5px', 'fontSize': '14px'})
    
    # État des filtres vide (pour compatibilité avec les callbacks)
    filter_status = html.Div(style={'display': 'none'})
    
    # Formater la valeur du filtre pour l'affichage
    display_value = filter_value
    
    if isinstance(filter_value, list):
        if filter_name == "Jour de la semaine":
            # Convertir indices en noms de jours
            jours = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"]
            day_names = [jours[i] for i in filter_value if 0 <= i < len(jours)]
            display_value = ", ".join(day_names)
        else:
            display_value = ", ".join(map(str, filter_value))
    elif isinstance(filter_value, tuple) and len(filter_value) == 2:
        display_value = f"de {filter_value[0]} à {filter_value[1]}"
    elif filter_name in ["Week-end", "Heure de nuit", "Heure ouvrée", "Jour férié", "Heure de pointe", 
                         "Nouvelle boucle", "DSP 1", "DEP_PEAG_OLT_match"]:
        display_value = filter_value
    
    # Ajouter message au chat
    current_time = datetime.now().strftime("%H:%M")
    
    # Message utilisateur dans le chat
    user_message = html.Div([
        html.Div(f"J'ai configuré le filtre {filter_name} : {display_value}",
                style=user_bubble_style),
        html.Small(current_time, 
                  style={'fontSize': '10px', 
                        'color': '#888', 
                        'marginTop': '5px', 
                        'display': 'block',
                        'textAlign': 'right',
                        'clear': 'both'})
    ])
    
    # Réponse de l'assistant dans le chat avec potentiellement la carte
    assistant_message_content = []
    
    # Ne pas afficher le nombre d'observations dans le chat
    assistant_message_content.append(
        html.Div(f"Filtre {filter_name} appliqué.",
                style={'marginBottom': '10px'})
    )
    
    # Si le filtre est sur le département ET qu'une valeur spécifique est sélectionnée
    if filter_name == "Département" and filter_value:
        # S'assurer que filter_value est une chaîne (code département)
        department_code = str(filter_value)
        # Ajouter la carte seulement si un département spécifique est sélectionné
        assistant_message_content.append(
            html.Div([
                html.P("Carte du département sélectionné :", 
                    style={
                        'fontWeight': 'bold', 
                        'marginTop': '15px', 
                        'marginBottom': '10px',
                        'fontSize': '14px'
                    }),
                create_france_map_with_department(department_code)
            ], style={
                'width': '100%',
                'display': 'flex',
                'flexDirection': 'column',
                'alignItems': 'center'
            })
        )
    
    # Ajouter les quatre boutons de statistiques
    assistant_message_content.append(html.Div([
        html.Button(
            [
                html.I(className="fas fa-network-wired", style={"marginRight": "8px"}),
                "Statistiques sur la structure du réseau"
            ],
            id="btn-structure-stats",
            style=stats_button_style
        ),
        html.Button(
            [
                html.I(className="fas fa-cog", style={"marginRight": "8px"}),
                "Statistiques sur les attributs techniques"
            ],
            id="btn-attributes-stats",
            style=stats_button_style
        ),
        html.Button(
            [
                html.I(className="fas fa-clock", style={"marginRight": "8px"}),
                "Statistiques temporelles"
            ],
            id="btn-temporal-stats",
            style=stats_button_style
        ),
        html.Button(
            [
                html.I(className="fas fa-tachometer-alt", style={"marginRight": "8px"}),
                "Agrégation et statistiques sur le temps DNS"
            ],
            id="btn-dns-stats",
            style=stats_button_style
        )
    ], style={'display': 'flex', 'flexDirection': 'column', 'gap': '10px', 'marginTop': '10px'}))
    
    assistant_message = html.Div([
        html.Div(assistant_message_content,
                style=assistant_bubble_style),
        html.Small(current_time, 
                  style={'fontSize': '10px', 
                        'color': '#888', 
                        'marginTop': '5px', 
                        'display': 'block',
                        'clear': 'both'})
    ])
    
    # Mettre à jour le chat
    updated_chat = chat_messages + [user_message, assistant_message]
    
    return updated_filters, stats_message, filter_status, updated_chat

# Callback pour réinitialiser tous les filtres
@callback(
    [Output('filter-values', 'data', allow_duplicate=True),
     Output('filter-stats', 'children', allow_duplicate=True),
     Output('filter-status', 'children', allow_duplicate=True),
     Output('chat-messages', 'children', allow_duplicate=True)],
    Input('reset-all-filters', 'n_clicks'),
    [State('chat-messages', 'children')],
    prevent_initial_call=True
)
def reset_all_filters(n_clicks, chat_messages):
    """
    Réinitialise tous les filtres appliqués
    """
    if not n_clicks:
        return {}, no_update, no_update, chat_messages
    
    # Réinitialiser les filtres
    empty_filters = {}
    
    # Message de statistiques réinitialisé
    stats_message = html.Div([
        html.I(className="fas fa-info-circle", style={'marginRight': '8px', 'color': sfr_colors['red']}),
        "Filtres réinitialisés"
    ], style={'backgroundColor': '#f0f0f0', 'padding': '10px', 'borderRadius': '5px', 'fontSize': '14px'})
    
    # Réinitialiser l'état des filtres (vide)
    filter_status = html.Div(style={'display': 'none'})
    
    # Ajouter message au chat
    current_time = datetime.now().strftime("%H:%M")
    
    # Message utilisateur dans le chat
    user_message = html.Div([
        html.Div("Je souhaite réinitialiser tous les filtres",
                style=user_bubble_style),
        html.Small(current_time, 
                  style={'fontSize': '10px', 
                        'color': '#888', 
                        'marginTop': '5px', 
                        'display': 'block',
                        'textAlign': 'right',
                        'clear': 'both'})
    ])
    
    # Réponse de l'assistant dans le chat
    assistant_message = html.Div([
        html.Div("Tous les filtres ont été réinitialisés.",
                style=assistant_bubble_style),
        html.Small(current_time, 
                  style={'fontSize': '10px', 
                        'color': '#888', 
                        'marginTop': '5px', 
                        'display': 'block',
                        'clear': 'both'})
    ])
    
    # Mettre à jour le chat
    updated_chat = chat_messages + [user_message, assistant_message]
    
    return empty_filters, stats_message, filter_status, updated_chat

# Callback pour mettre à jour dynamiquement les options des filtres
@callback(
    [Output({'type': 'filter-component', 'name': ALL}, 'options'),
     Output({'type': 'filter-component', 'name': ALL}, 'value')],
    [Input('filter-values', 'data')],
    [State({'type': 'filter-component', 'name': ALL}, 'id'),
     State({'type': 'filter-component', 'name': ALL}, 'value')]
)
def update_filter_options(filter_values, filter_ids, current_values):
    """
    Met à jour les options disponibles pour tous les filtres
    en fonction des filtres déjà appliqués
    """
    if not filter_values:
        return [no_update] * len(filter_ids), [no_update] * len(filter_ids)
    
    # Préparation des listes pour les outputs
    updated_options = []
    updated_values = []
    
    # Pour chaque filtre configuré
    for i, filter_id in enumerate(filter_ids):
        filter_name = filter_id['name']
        current_value = current_values[i]
        
        # Ne pas inclure le filtre lui-même dans les filtres actuels pour sa propre mise à jour
        current_filters = {k: v for k, v in filter_values.items() if k != filter_name}
        
        # Obtenir les nouvelles options pour ce filtre
        new_options = data_manager.get_filter_options(filter_name, current_filters)
        
        # Préparer les options pour différents types de composants
        if filter_name == "Date":
            # Options pour le DatePickerRange
            updated_options.append(no_update)  # DatePickerRange n'a pas d'options à mettre à jour
            updated_values.append(current_value)
        
        elif filter_name == "Heure":
            # Options pour le RangeSlider d'heure - CORRECTION DE L'ERREUR
            if isinstance(new_options, list) and len(new_options) == 2:
                min_hour, max_hour = new_options
                updated_options.append({
                    'min': min_hour,
                    'max': max_hour,
                    'marks': {i: f"{i}h" for i in range(min_hour, max_hour+1, 2)}
                })
                
                # Ajuster la valeur si nécessaire
                if current_value:
                    updated_value = [
                        max(min_hour, current_value[0]),
                        min(max_hour, current_value[1])
                    ]
                else:
                    updated_value = [min_hour, max_hour]
                updated_values.append(updated_value)
            else:
                # Valeurs par défaut si new_options est vide ou invalide
                updated_options.append({
                    'min': 0,
                    'max': 23,
                    'marks': {i: f"{i}h" for i in range(0, 24, 2)}
                })
                updated_values.append([0, 23] if not current_value else current_value)
        
        elif filter_name == "Jour de la semaine":
            # Pas de changement nécessaire pour les options des jours de la semaine
            updated_options.append(no_update)
            updated_values.append(current_value)
        
        elif filter_name in ["Week-end", "Heure de nuit", "Heure ouvrée", "Jour férié", 
                           "Heure de pointe", "Nouvelle boucle", "DSP 1", "DEP_PEAG_OLT_match"]:
            # Pas de changement nécessaire pour les options des filtres booléens
            updated_options.append(no_update)
            updated_values.append(current_value)
        
        elif filter_name == "Nombre de clients":
            # Options pour le RangeSlider de clients - CORRECTION DE L'ERREUR
            if isinstance(new_options, list) and len(new_options) == 2:
                min_val, max_val = new_options
                # Éviter division par zéro ou valeurs négatives
                range_step = max(1, int((max_val - min_val) / 5)) if max_val > min_val else 1
                
                updated_options.append({
                    'min': min_val,
                    'max': max_val,
                    'marks': {i: str(i) for i in range(int(min_val), int(max_val)+1, range_step)},
                    'step': max(0.1, (max_val - min_val) / 100) if max_val > min_val else 0.1
                })
                
                # Ajuster la valeur si nécessaire
                if current_value:
                    updated_value = [
                        max(min_val, current_value[0]),
                        min(max_val, current_value[1])
                    ]
                else:
                    updated_value = [min_val, max_val]
                updated_values.append(updated_value)
            else:
                # Valeurs par défaut
                updated_options.append({
                    'min': 0,
                    'max': 1000,
                    'marks': {i: str(i) for i in range(0, 1001, 200)},
                    'step': 10
                })
                updated_values.append([0, 1000] if not current_value else current_value)
        
        else:
            # Dropdown par défaut
            if isinstance(new_options, list) and new_options:
                updated_options.append([{"label": opt, "value": opt} for opt in new_options])
                
                # Vérifier si la valeur actuelle est toujours dans les options
                if current_value and current_value not in new_options:
                    updated_values.append(None)
                else:
                    updated_values.append(current_value)
            else:
                updated_options.append([])
                updated_values.append(None)
    
    return updated_options, updated_values

# Callback pour gérer le clic sur le bouton de statistiques de structure

# Imports nécessaires (à placer en haut du fichier si ce n'est pas déjà fait)
from dash import Input, Output, State, callback, html, dcc, ALL, MATCH, ctx, no_update
import dash_bootstrap_components as dbc
import pandas as pd
from datetime import datetime
from styles.theme import sfr_colors
from utils.data_loader import DataManager
from utils.graph_utils import (
    create_structure_stats_graphs, 
    create_attributes_stats_graphs,
    create_temporal_stats_graphs,
    create_france_map_with_department
)

# Obtenir l'instance du gestionnaire de données
data_manager = DataManager.get_instance()

# Callback pour gérer le clic sur le bouton de statistiques de structure
@callback(
    Output('chat-messages', 'children', allow_duplicate=True),
    Input('btn-structure-stats', 'n_clicks'),
    [State('filter-values', 'data'),
     State('chat-messages', 'children')],
    prevent_initial_call=True
)
def display_structure_stats(n_clicks, current_filters, chat_messages):
    """
    Affiche les graphiques statistiques de structure lorsque le bouton est cliqué
    et ajoute les boutons de statistiques après les graphiques
    """
    if not n_clicks or not current_filters:
        return chat_messages
    
    # Obtenir les données filtrées
    filtered_df = data_manager.filter_dataframe(current_filters)
    
    # Créer les graphiques (en passant les filtres actuels)
    stats_graphs = create_structure_stats_graphs(filtered_df, current_filters)
    
    # Date et heure actuelles
    current_time = datetime.now().strftime("%H:%M")
    
    # Message utilisateur dans le chat
    user_message = html.Div([
        html.Div("Je souhaite voir les statistiques de structure du réseau",
                style=user_bubble_style),
        html.Small(current_time, 
                  style={'fontSize': '10px', 
                        'color': '#888', 
                        'marginTop': '5px', 
                        'display': 'block',
                        'textAlign': 'right',
                        'clear': 'both'})
    ])
    
    # Message de l'assistant avec les graphiques
    assistant_content = [
        html.Div("Voici les statistiques sur la structure du réseau :",
                style={'marginBottom': '15px'})
    ]
    
    # Ajouter les graphiques au contenu de l'assistant
    assistant_content.extend(stats_graphs)
    
    # Ajouter les quatre boutons de statistiques après les graphiques
    assistant_content.append(html.Div([
        html.Div("Souhaitez-vous explorer d'autres statistiques ?", 
                style={'marginTop': '25px', 'marginBottom': '15px', 'fontWeight': 'bold'}),
        html.Button(
            [
                html.I(className="fas fa-network-wired", style={"marginRight": "8px"}),
                "Statistiques sur la structure du réseau"
            ],
            id="btn-structure-stats",
            style=stats_button_style
        ),
        html.Button(
            [
                html.I(className="fas fa-cog", style={"marginRight": "8px"}),
                "Statistiques sur les attributs techniques"
            ],
            id="btn-attributes-stats",
            style=stats_button_style
        ),
        html.Button(
            [
                html.I(className="fas fa-clock", style={"marginRight": "8px"}),
                "Statistiques temporelles"
            ],
            id="btn-temporal-stats",
            style=stats_button_style
        ),
        html.Button(
            [
                html.I(className="fas fa-tachometer-alt", style={"marginRight": "8px"}),
                "Agrégation et statistiques sur le temps DNS"
            ],
            id="btn-dns-stats",
            style=stats_button_style
        )
    ], style={'display': 'flex', 'flexDirection': 'column', 'gap': '10px', 'marginTop': '15px', 'marginBottom': '10px',
              'backgroundColor': '#f9f9f9', 'padding': '15px', 'borderRadius': '8px'}))
    
    # Message de l'assistant
    assistant_message = html.Div([
        html.Div(assistant_content,
                style=assistant_bubble_style),
        html.Small(current_time, 
                  style={'fontSize': '10px', 
                        'color': '#888', 
                        'marginTop': '5px', 
                        'display': 'block',
                        'clear': 'both'})
    ])
    
    # Mettre à jour le chat
    updated_chat = chat_messages + [user_message, assistant_message]
    
    return updated_chat

# Callback pour gérer le clic sur le bouton de statistiques d'attributs
@callback(
    Output('chat-messages', 'children', allow_duplicate=True),
    Input('btn-attributes-stats', 'n_clicks'),
    [State('filter-values', 'data'),
     State('chat-messages', 'children')],
    prevent_initial_call=True
)
def display_attributes_stats(n_clicks, current_filters, chat_messages):
    """
    Affiche les graphiques statistiques d'attributs lorsque le bouton est cliqué
    et ajoute les boutons de statistiques après les graphiques
    """
    if not n_clicks or not current_filters:
        return chat_messages
    
    # Obtenir les données filtrées
    filtered_df = data_manager.filter_dataframe(current_filters)
    
    # Créer les graphiques
    stats_graphs = create_attributes_stats_graphs(filtered_df)
    
    # Date et heure actuelles
    current_time = datetime.now().strftime("%H:%M")
    
    # Message utilisateur dans le chat
    user_message = html.Div([
        html.Div("Je souhaite voir les statistiques des attributs techniques",
                style=user_bubble_style),
        html.Small(current_time, 
                  style={'fontSize': '10px', 
                        'color': '#888', 
                        'marginTop': '5px', 
                        'display': 'block',
                        'textAlign': 'right',
                        'clear': 'both'})
    ])
    
    # Message de l'assistant avec les graphiques
    assistant_content = [
        html.Div("Voici les statistiques sur les attributs techniques (modèle d'OLT, nouvelle boucle, etc.) :",
                style={'marginBottom': '15px'})
    ]
    
    # Ajouter les graphiques au contenu de l'assistant
    assistant_content.extend(stats_graphs)
    
    # Ajouter les quatre boutons de statistiques après les graphiques
    assistant_content.append(html.Div([
        html.Div("Souhaitez-vous explorer d'autres statistiques ?", 
                style={'marginTop': '25px', 'marginBottom': '15px', 'fontWeight': 'bold'}),
        html.Button(
            [
                html.I(className="fas fa-network-wired", style={"marginRight": "8px"}),
                "Statistiques sur la structure du réseau"
            ],
            id="btn-structure-stats",
            style=stats_button_style
        ),
        html.Button(
            [
                html.I(className="fas fa-cog", style={"marginRight": "8px"}),
                "Statistiques sur les attributs techniques"
            ],
            id="btn-attributes-stats",
            style=stats_button_style
        ),
        html.Button(
            [
                html.I(className="fas fa-clock", style={"marginRight": "8px"}),
                "Statistiques temporelles"
            ],
            id="btn-temporal-stats",
            style=stats_button_style
        ),
        html.Button(
            [
                html.I(className="fas fa-tachometer-alt", style={"marginRight": "8px"}),
                "Agrégation et statistiques sur le temps DNS"
            ],
            id="btn-dns-stats",
            style=stats_button_style
        )
    ], style={'display': 'flex', 'flexDirection': 'column', 'gap': '10px', 'marginTop': '15px', 'marginBottom': '10px',
              'backgroundColor': '#f9f9f9', 'padding': '15px', 'borderRadius': '8px'}))
    
    # Message de l'assistant
    assistant_message = html.Div([
        html.Div(assistant_content,
                style=assistant_bubble_style),
        html.Small(current_time, 
                  style={'fontSize': '10px', 
                        'color': '#888', 
                        'marginTop': '5px', 
                        'display': 'block',
                        'clear': 'both'})
    ])
    
    # Mettre à jour le chat
    updated_chat = chat_messages + [user_message, assistant_message]
    
    return updated_chat

# Callback pour gérer le clic sur le bouton de statistiques temporelles
@callback(
    Output('chat-messages', 'children', allow_duplicate=True),
    Input('btn-temporal-stats', 'n_clicks'),
    [State('filter-values', 'data'),
     State('chat-messages', 'children')],
    prevent_initial_call=True
)
def display_temporal_stats(n_clicks, current_filters, chat_messages):
    """
    Affiche les graphiques statistiques temporels lorsque le bouton est cliqué
    et ajoute les boutons de statistiques après les graphiques
    """
    if not n_clicks or not current_filters:
        return chat_messages
    
    # Obtenir les données filtrées
    filtered_df = data_manager.filter_dataframe(current_filters)
    
    # Créer les graphiques
    stats_graphs = create_temporal_stats_graphs(filtered_df)
    
    # Date et heure actuelles
    current_time = datetime.now().strftime("%H:%M")
    
    # Message utilisateur dans le chat
    user_message = html.Div([
        html.Div("Je souhaite voir les statistiques temporelles",
                style=user_bubble_style),
        html.Small(current_time, 
                  style={'fontSize': '10px', 
                        'color': '#888', 
                        'marginTop': '5px', 
                        'display': 'block',
                        'textAlign': 'right',
                        'clear': 'both'})
    ])
    
    # Message de l'assistant avec les graphiques
    assistant_content = [
        html.Div("Voici les statistiques temporelles (jour, heure, week-end vs semaine, etc.) :",
                style={'marginBottom': '15px'})
    ]
    
    # Ajouter les graphiques au contenu de l'assistant
    assistant_content.extend(stats_graphs)
    
    # Ajouter les quatre boutons de statistiques après les graphiques
    assistant_content.append(html.Div([
        html.Div("Souhaitez-vous explorer d'autres statistiques ?", 
                style={'marginTop': '25px', 'marginBottom': '15px', 'fontWeight': 'bold'}),
        html.Button(
            [
                html.I(className="fas fa-network-wired", style={"marginRight": "8px"}),
                "Statistiques sur la structure du réseau"
            ],
            id="btn-structure-stats",
            style=stats_button_style
        ),
        html.Button(
            [
                html.I(className="fas fa-cog", style={"marginRight": "8px"}),
                "Statistiques sur les attributs techniques"
            ],
            id="btn-attributes-stats",
            style=stats_button_style
        ),
        html.Button(
            [
                html.I(className="fas fa-clock", style={"marginRight": "8px"}),
                "Statistiques temporelles"
            ],
            id="btn-temporal-stats",
            style=stats_button_style
        ),
        html.Button(
            [
                html.I(className="fas fa-tachometer-alt", style={"marginRight": "8px"}),
                "Agrégation et statistiques sur le temps DNS"
            ],
            id="btn-dns-stats",
            style=stats_button_style
        )
    ], style={'display': 'flex', 'flexDirection': 'column', 'gap': '10px', 'marginTop': '15px', 'marginBottom': '10px',
              'backgroundColor': '#f9f9f9', 'padding': '15px', 'borderRadius': '8px'}))
    
    # Message de l'assistant
    assistant_message = html.Div([
        html.Div(assistant_content,
                style=assistant_bubble_style),
        html.Small(current_time, 
                  style={'fontSize': '10px', 
                        'color': '#888', 
                        'marginTop': '5px', 
                        'display': 'block',
                        'clear': 'both'})
    ])
    
    # Mettre à jour le chat
    updated_chat = chat_messages + [user_message, assistant_message]
    
    return updated_chat

# Callback pour gérer le clic sur le bouton de statistiques DNS
@callback(
    Output('chat-messages', 'children', allow_duplicate=True),
    Input('btn-dns-stats', 'n_clicks'),
    [State('filter-values', 'data'),
     State('chat-messages', 'children')],
    prevent_initial_call=True
)
def display_dns_aggregation_options(n_clicks, current_filters, chat_messages):
    """
    Affiche les options d'agrégation pour les statistiques DNS
    """
    if not n_clicks or not current_filters:
        return chat_messages
    
    # Date et heure actuelles
    current_time = datetime.now().strftime("%H:%M")
    
    # Message utilisateur dans le chat
    user_message = html.Div([
        html.Div("Je souhaite voir les statistiques sur le temps moyen des tests DNS",
                style=user_bubble_style),
        html.Small(current_time, 
                  style={'fontSize': '10px', 
                        'color': '#888', 
                        'marginTop': '5px', 
                        'display': 'block',
                        'textAlign': 'right',
                        'clear': 'both'})
    ])
    
    # Contenu de l'assistant avec les options d'agrégation
    assistant_content = [
        html.Div("Veuillez sélectionner les dimensions d'agrégation pour analyser le temps moyen DNS :",
                style={'marginBottom': '15px'})
    ]
    
    # Options d'agrégation (cases à cocher)
    aggregation_options = html.Div([
        html.Div([
            html.Label("Dimensions d'agrégation :", 
                     style={'fontWeight': 'bold', 'marginBottom': '10px'}),
            dcc.Checklist(
                id='dns-aggregation-dims',
                options=[
                    {'label': 'Département', 'value': 'code_departement'},
                    {'label': 'Boucle', 'value': 'boucle'},
                    {'label': 'PEAG', 'value': 'peag_nro'},
                    {'label': 'OLT', 'value': 'olt_name'},
                    {'label': 'PEBIB', 'value': 'pebib'}
                ],
                value=['code_departement', 'peag_nro', 'olt_name'],  # Valeurs par défaut
                style={'marginBottom': '15px'}
            )
        ], style={'marginBottom': '15px'}),
        
        # Bouton pour lancer l'analyse
        html.Button(
            "Générer les statistiques DNS",
            id='generate-dns-stats',
            style={
                'backgroundColor': sfr_colors['red'],
                'color': 'white',
                'border': 'none',
                'padding': '10px 15px',
                'borderRadius': '5px',
                'cursor': 'pointer',
                'fontWeight': 'bold'
            }
        )
    ], style={'backgroundColor': '#f9f9f9', 'padding': '15px', 'borderRadius': '8px'})
    
    assistant_content.append(aggregation_options)
    
    # Message de l'assistant
    assistant_message = html.Div([
        html.Div(assistant_content,
                style=assistant_bubble_style),
        html.Small(current_time, 
                  style={'fontSize': '10px', 
                        'color': '#888', 
                        'marginTop': '5px', 
                        'display': 'block',
                        'clear': 'both'})
    ])
    
    # Mettre à jour le chat
    updated_chat = chat_messages + [user_message, assistant_message]
    
    return updated_chat

@callback(
    Output('chat-messages', 'children', allow_duplicate=True),
    Input('generate-dns-stats', 'n_clicks'),
    [State('dns-aggregation-dims', 'value'),
     State('filter-values', 'data'),
     State('chat-messages', 'children')],
    prevent_initial_call=True
)
def generate_dns_stats(n_clicks, aggregation_dims, current_filters, chat_messages):
    """
    Génère les statistiques DNS en fonction des dimensions d'agrégation sélectionnées
    Affiche les 20 combinaisons avec le temps DNS moyen le plus élevé
    """
    if not n_clicks or not aggregation_dims:
        return chat_messages
    
    # Obtenir les données filtrées
    filtered_df = data_manager.filter_dataframe(current_filters)
    
    # Date et heure actuelles
    current_time = datetime.now().strftime("%H:%M")
    
    # Message utilisateur
    user_message = html.Div([
        html.Div(f"Je souhaite générer les statistiques DNS avec agrégation par : {', '.join(aggregation_dims)}",
                style=user_bubble_style),
        html.Small(current_time, 
                  style={'fontSize': '10px', 
                        'color': '#888', 
                        'marginTop': '5px', 
                        'display': 'block',
                        'textAlign': 'right',
                        'clear': 'both'})
    ])
    
    # Styles uniformisés pour les titres et textes
    SECTION_TITLE_STYLE = {
        'fontSize': '16px',
        'fontWeight': 'bold',
        'marginTop': '20px',
        'marginBottom': '15px',
        'color': '#000000'  # Noir pour tous les titres
    }
    
    SUBSECTION_TITLE_STYLE = {
        'fontSize': '14px',
        'fontWeight': 'bold',
        'marginTop': '15px',
        'marginBottom': '10px',
        'color': '#000000'  # Noir pour tous les sous-titres
    }
    
    GRAPH_TITLE_FONT = dict(
        size=15,
        color='#000000',  # Noir pour les titres de graphiques
        family='Arial, sans-serif'
    )
    
    GRAPH_FONT = dict(
        size=13,
        color='#000000',
        family='Arial, sans-serif'
    )
    
    GRAPH_CONTAINER_STYLE = {
        'marginBottom': '25px', 
        'border': '1px solid #ddd', 
        'borderRadius': '8px', 
        'padding': '15px', 
        'backgroundColor': 'white',
        'boxShadow': '0 2px 5px rgba(0,0,0,0.05)',
        'width': '100%'
    }
    
    # Préparation et calcul des statistiques
    try:
        # Vérifier les colonnes disponibles
        print("Colonnes disponibles:", filtered_df.columns.tolist())
        
        # Identifier les colonnes pour jour, heure et date
        jour_col = "day_of_week" if "day_of_week" in filtered_df.columns else "jour"
        heure_col = "heure" if "heure" in filtered_df.columns else "hour"
        date_col = "date" if "date" in filtered_df.columns else "date_hour"
        
        # Colonnes requises adaptées aux noms réels
        required_cols = [jour_col, heure_col, "avg_dns_time", "nb_test_dns"]
        if date_col in filtered_df.columns:
            required_cols.append(date_col)
        
        # Nettoyer les données avec les noms de colonnes corrects
        df_cleaned = filtered_df.dropna(subset=required_cols + aggregation_dims).copy()
        
        if len(df_cleaned) == 0:
            assistant_content = [
                html.Div("Aucune donnée disponible après filtrage pour l'analyse DNS", 
                         style={'color': '#000000', 'fontWeight': 'bold', 'margin': '20px 0'})
            ]
        else:
            # Si nous avons une colonne de date, nous l'utiliserons pour l'axe X
            # Sinon, nous créerons une série temporelle à partir de jour et heure
            if date_col in df_cleaned.columns:
                # S'assurer que la colonne date est au format datetime
                df_cleaned[date_col] = pd.to_datetime(df_cleaned[date_col])
                
                # Dimensions d'agrégation avec la date
                all_dims = [date_col] + aggregation_dims
            else:
                # Dimensions d'agrégation avec jour et heure
                all_dims = [jour_col, heure_col] + aggregation_dims
            
            # Agrégation avec moyenne pondérée
            df_grouped = df_cleaned.groupby(all_dims).agg(
                moy_avg_dns_time=(
                    "avg_dns_time",
                    lambda x: (
                        (x * df_cleaned.loc[x.index, "nb_test_dns"]).sum()
                        / df_cleaned.loc[x.index, "nb_test_dns"].sum()
                    ) if df_cleaned.loc[x.index, "nb_test_dns"].sum() > 0 else None
                ),
                total_tests_dns=("nb_test_dns", "sum")
            ).reset_index()
            
            # Si nous utilisons jour et heure, créons une colonne datetime
            if date_col not in df_grouped.columns:
                # Créer une date de référence (pour combiner avec jour et heure)
                base_date = pd.Timestamp('2023-01-01')  # Date arbitraire (un dimanche)
                
                # Créer une colonne datetime en combinant la date de référence, le jour de la semaine et l'heure
                df_grouped['datetime'] = df_grouped.apply(
                    lambda row: base_date + pd.Timedelta(days=int(row[jour_col])) + pd.Timedelta(hours=int(row[heure_col])),
                    axis=1
                )
                x_col = 'datetime'
            else:
                x_col = date_col
            
            # Statistiques générales
            dns_avg = df_grouped["moy_avg_dns_time"].mean()
            dns_median = df_grouped["moy_avg_dns_time"].median()
            dns_min = df_grouped["moy_avg_dns_time"].min()
            dns_max = df_grouped["moy_avg_dns_time"].max()
            total_tests = df_grouped["total_tests_dns"].sum()
            
            # Contenu de l'assistant
            assistant_content = [
                html.Div(f"Statistiques DNS agrégées par {', '.join(aggregation_dims)}", style=SECTION_TITLE_STYLE)
            ]
            
            # Statistiques résumées
            stats_summary = html.Div([
                html.Div([
                    html.Div([
                        html.Div("Temps moyen", style={"fontWeight": "bold", "marginBottom": "5px", "color": "#000000"}),
                        html.Div(f"{dns_avg:.2f} ms", style={"fontSize": "18px", "color": "#000000"})
                    ], style={'padding': '10px', 'backgroundColor': 'white', 'borderRadius': '5px', 'flex': '1', 'textAlign': 'center'}),
                    
                    html.Div([
                        html.Div("Temps médian", style={"fontWeight": "bold", "marginBottom": "5px", "color": "#000000"}),
                        html.Div(f"{dns_median:.2f} ms", style={"fontSize": "18px", "color": "#000000"})
                    ], style={'padding': '10px', 'backgroundColor': 'white', 'borderRadius': '5px', 'flex': '1', 'textAlign': 'center'}),
                    
                    html.Div([
                        html.Div("Temps min", style={"fontWeight": "bold", "marginBottom": "5px", "color": "#000000"}),
                        html.Div(f"{dns_min:.2f} ms", style={"fontSize": "18px", "color": "#000000"})
                    ], style={'padding': '10px', 'backgroundColor': 'white', 'borderRadius': '5px', 'flex': '1', 'textAlign': 'center'}),
                    
                    html.Div([
                        html.Div("Temps max", style={"fontWeight": "bold", "marginBottom": "5px", "color": "#000000"}),
                        html.Div(f"{dns_max:.2f} ms", style={"fontSize": "18px", "color": "#000000"})
                    ], style={'padding': '10px', 'backgroundColor': 'white', 'borderRadius': '5px', 'flex': '1', 'textAlign': 'center'}),
                    
                    html.Div([
                        html.Div("Total tests DNS", style={"fontWeight": "bold", "marginBottom": "5px", "color": "#000000"}),
                        html.Div(f"{total_tests:,}".replace(',', ' '), style={"fontSize": "18px", "color": "#000000"})
                    ], style={'padding': '10px', 'backgroundColor': 'white', 'borderRadius': '5px', 'flex': '1', 'textAlign': 'center'})
                ], style={'display': 'flex', 'flexWrap': 'wrap', 'gap': '10px', 'marginBottom': '20px'})
            ], style={'backgroundColor': '#f5f5f5', 'padding': '15px', 'borderRadius': '5px', 'marginBottom': '20px'})
            
            assistant_content.append(stats_summary)
            
            # Créer un identifiant de combinaison unique pour chaque ensemble de dimensions d'agrégation
            df_grouped['combination'] = df_grouped.apply(
                lambda row: "-".join([str(row[dim]) for dim in aggregation_dims]),
                axis=1
            )
            
            # Trouver les 20 combinaisons avec le temps DNS moyen le plus élevé
            combo_avg_dns = df_grouped.groupby('combination')['moy_avg_dns_time'].mean().reset_index()
            top_combinations = combo_avg_dns.sort_values('moy_avg_dns_time', ascending=False).head(20)['combination'].tolist()
            
            # Titre de section pour les top combinaisons
            assistant_content.append(html.Div(
                "Top 20 des combinaisons avec le temps DNS moyen le plus élevé", 
                style=SECTION_TITLE_STYLE
            ))
            
            # Créer un graphique pour chaque combinaison problématique
            for combination in top_combinations:
                # Filtrer les données pour cette combinaison
                combo_data = df_grouped[df_grouped['combination'] == combination]
                
                # Créer une version lisible de la combinaison
                readable_parts = []
                combination_values = combination.split("-")
                
                for i, dim in enumerate(aggregation_dims):
                    if i < len(combination_values):
                        dim_name = dim.replace('_', ' ').title()
                        readable_parts.append(f"{dim_name}: {combination_values[i]}")
                
                readable_combo = " | ".join(readable_parts)
                
                # Calculer les statistiques pour cette combinaison
                avg_time = combo_data['moy_avg_dns_time'].mean()
                max_time = combo_data['moy_avg_dns_time'].max()
                total_tests = combo_data['total_tests_dns'].sum()
                
                # Sous-titre pour cette combinaison
                assistant_content.append(html.Div(
                    readable_combo,
                    style=SUBSECTION_TITLE_STYLE
                ))
                
                # Afficher les statistiques clés pour cette combinaison
                stats_container = html.Div([
                    html.Div([
                        html.Div("Temps moyen", style={"fontWeight": "bold", "color": "#000000"}),
                        html.Div(f"{avg_time:.2f} ms", style={"fontSize": "16px", "color": "#000000"})
                    ], style={'padding': '10px', 'backgroundColor': '#f8f8f8', 'borderRadius': '5px', 'textAlign': 'center', 'flex': '1'}),
                    
                    html.Div([
                        html.Div("Temps max", style={"fontWeight": "bold", "color": "#000000"}),
                        html.Div(f"{max_time:.2f} ms", style={"fontSize": "16px", "color": "#000000"})
                    ], style={'padding': '10px', 'backgroundColor': '#f8f8f8', 'borderRadius': '5px', 'textAlign': 'center', 'flex': '1'}),
                    
                    html.Div([
                        html.Div("Total tests", style={"fontWeight": "bold", "color": "#000000"}),
                        html.Div(f"{total_tests:,}".replace(',', ' '), style={"fontSize": "16px", "color": "#000000"})
                    ], style={'padding': '10px', 'backgroundColor': '#f8f8f8', 'borderRadius': '5px', 'textAlign': 'center', 'flex': '1'})
                ], style={'display': 'flex', 'gap': '10px', 'marginBottom': '10px'})
                
                # Créer un graphique d'évolution temporelle pour cette combinaison
                combo_data_sorted = combo_data.sort_values(by=x_col)
                
                fig = px.line(
                    combo_data_sorted,
                    x=x_col,
                    y='moy_avg_dns_time',
                    title=f"Évolution temporelle du temps DNS",
                    labels={
                        x_col: "Date/Heure",
                        'moy_avg_dns_time': "Temps DNS moyen (ms)"
                    },
                    color_discrete_sequence=["#e2001a"]
                )
                
                # Mise en forme du graphique
                fig.update_traces(
                    mode="lines+markers",
                    marker=dict(size=6),
                    line=dict(width=2)
                )
                
                fig.update_layout(
                    height=350,
                    margin={"r": 20, "t": 50, "l": 20, "b": 50},
                    font=GRAPH_FONT,
                    title_font=GRAPH_TITLE_FONT,
                    plot_bgcolor='white',
                    showlegend=False
                )
                
                # Ajouter une ligne horizontale indiquant la moyenne globale pour référence
                fig.add_hline(
                    y=dns_avg,
                    line_dash="dash",
                    line_color="gray",
                    annotation_text="Moyenne globale",
                    annotation_position="bottom right"
                )
                
                # Ajouter les statistiques et le graphique pour cette combinaison
                combo_container = html.Div([
                    stats_container,
                    dcc.Graph(figure=fig, config={'displayModeBar': False})
                ], style=GRAPH_CONTAINER_STYLE)
                
                assistant_content.append(combo_container)
                
    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f"Erreur lors de la création du graphique DNS: {e}")
        assistant_content = [
            html.Div(f"Erreur lors de la génération des statistiques DNS: {str(e)}", 
                     style={'color': '#000000', 'fontWeight': 'bold', 'margin': '20px 0'})
        ]
    
    # Message de l'assistant
    assistant_message = html.Div([
        html.Div(assistant_content,
                style=assistant_bubble_style),
        html.Small(current_time, 
                  style={'fontSize': '10px', 
                        'color': '#888', 
                        'marginTop': '5px', 
                        'display': 'block',
                        'clear': 'both'})
    ])
    
    # Mettre à jour le chat avec le premier message
    updated_chat = chat_messages + [user_message, assistant_message]
    
    # Créer une nouvelle réponse de l'assistant avec les 4 boutons
    buttons_time = datetime.now().strftime("%H:%M")
    
    # Boutons de statistiques
    buttons_content = [
        html.Div("Souhaitez-vous explorer d'autres statistiques ?",
                style={'marginBottom': '10px', 'fontWeight': 'bold', 'color': '#000000'})
    ]
    
    # Ajouter les quatre boutons de statistiques
    buttons_content.append(html.Div([
        html.Button(
            [
                html.I(className="fas fa-network-wired", style={"marginRight": "8px"}),
                "Statistiques sur la structure du réseau"
            ],
            id="btn-structure-stats",
            style=stats_button_style
        ),
        html.Button(
            [
                html.I(className="fas fa-cog", style={"marginRight": "8px"}),
                "Statistiques sur les attributs techniques"
            ],
            id="btn-attributes-stats",
            style=stats_button_style
        ),
        html.Button(
            [
                html.I(className="fas fa-clock", style={"marginRight": "8px"}),
                "Statistiques temporelles"
            ],
            id="btn-temporal-stats",
            style=stats_button_style
        ),
        html.Button(
            [
                html.I(className="fas fa-tachometer-alt", style={"marginRight": "8px"}),
                "Agrégation et statistiques sur le temps DNS"
            ],
            id="btn-dns-stats",
            style=stats_button_style
        )
    ], style={'display': 'flex', 'flexDirection': 'column', 'gap': '10px', 'marginTop': '10px'}))
    
    buttons_message = html.Div([
        html.Div(buttons_content,
                style=assistant_bubble_style),
        html.Small(buttons_time, 
                  style={'fontSize': '10px', 
                        'color': '#888', 
                        'marginTop': '5px', 
                        'display': 'block',
                        'clear': 'both'})
    ])
    
    # Ajouter cette réponse supplémentaire à la conversation
    updated_chat = updated_chat + [buttons_message]
    
    return updated_chat