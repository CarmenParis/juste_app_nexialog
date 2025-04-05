# utils/graph_utils.py
from dash import html, dcc
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from styles.theme import sfr_colors
import dash_bootstrap_components as dbc

# Styles uniformisés pour les éléments de graphiques
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
    'marginTop': '20px',
    'marginBottom': '15px',
    'color': '#000000'  # Noir pour tous les sous-titres
}

DETAIL_TITLE_STYLE = {
    'fontWeight': 'bold',
    'marginTop': '20px',
    'marginBottom': '10px',
    'color': '#000000',  # Noir
    'fontSize': '14px'
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

def create_bar_chart(df, column, title_prefix, limit=20):
    """
    Crée un graphique à barres horizontal qui utilise presque toute la largeur du chat
    Version améliorée avec meilleure visibilité des nombres
    """
    from dash import html, dcc
    import plotly.express as px
    
    counts = df[column].value_counts().reset_index()
    readable_column = column.replace('_', ' ').title()
    counts.columns = [readable_column, 'Nombre d\'observations']
    
    # Limiter le nombre de valeurs affichées
    if len(counts) > limit:
        counts = counts.head(limit)
        title = f"{title_prefix} par {readable_column} (Top {limit})"
    else:
        title = f"{title_prefix} par {readable_column}"
    
    # Créer le graphique avec des barres horizontales avec taille actuelle
    fig = px.bar(
        counts, 
        y=readable_column,  # Barres horizontales (catégories en Y)
        x='Nombre d\'observations',  # Valeurs en X
        title=title,
        color='Nombre d\'observations',
        color_continuous_scale=[[0, "#003399"], [1, "#e2001a"]],
        height=max(400, len(counts) * 25)  # Hauteur adaptée au nombre d'éléments
    )
    
    # Obtenir la valeur maximale pour ajuster l'axe X
    max_val = counts['Nombre d\'observations'].max()
    
    # Configurer la mise en page avec une marge droite élargie
    fig.update_layout(
        margin={"r": 120, "t": 40, "l": 150, "b": 40},  # Augmentation significative de la marge droite
        xaxis_title="Nombre d'observations",
        yaxis_title=None,
        font=GRAPH_FONT,
        title_font=GRAPH_TITLE_FONT,
        plot_bgcolor='white',
        width=900,  # Largeur fixe du graphique
        xaxis=dict(
            range=[0, max_val * 1.20]  # Ajouter 20% d'espace à droite
        )
    )
    
    # Ajouter les valeurs sur les barres avec positionnement amélioré
    fig.update_traces(
        texttemplate='<b>%{x}</b>',  # Texte en gras
        textposition='outside',  # Toujours positionner le texte à l'extérieur des barres
        cliponaxis=False,  # Empêcher que le texte soit coupé
        textfont=dict(size=14, color='black'),  # Police plus grande et bien visible
        hovertemplate='%{y}: %{x} observations<extra></extra>'
    )
    
    # Container amélioré avec largeur complète
    return html.Div([
        dcc.Graph(
            figure=fig, 
            config={'displayModeBar': False, 'responsive': True},
            style={'width': '100%'}  # Utiliser toute la largeur disponible
        )
    ], style={
        'marginBottom': '25px', 
        'border': '1px solid #ddd', 
        'borderRadius': '8px', 
        'padding': '15px', 
        'backgroundColor': 'white',
        'boxShadow': '0 2px 5px rgba(0,0,0,0.05)',
        'width': '100%'  # Conteneur utilisant toute la largeur
    })

def create_structure_stats_graphs(filtered_df, current_filters):
    """
    Crée des graphiques statistiques liés à la structure technique:
    1. Graphiques simples du nombre d'observations
    2. Graphiques optimisés pour les croisements les plus importants
    
    Version améliorée avec graphiques élargis et titres en noir
    """
    import pandas as pd
    from dash import html, dcc
    import plotly.express as px
    import plotly.graph_objects as go
    from styles.theme import sfr_colors
    
    graphs = []
    
    # Liste complète des colonnes de structure dans l'ordre hiérarchique
    structure_hierarchy = [
        ('Département', 'code_departement'),
        ('Boucle', 'boucle'),
        ('Identifiant de PEAG', 'peag_nro'),
        ('Identifiant d\'OLT', 'olt_name'),
        ('PEBIB', 'pebib'),
        ('POP DNS', 'pop_dns')
    ]
    
    # Dictionnaire pour faciliter la conversion
    structure_columns = dict(structure_hierarchy)
    
    # Convertir les noms de filtres en noms de colonnes
    applied_columns = []
    for filter_name in current_filters.keys():
        if filter_name in structure_columns:
            applied_columns.append(structure_columns[filter_name])
        elif filter_name in structure_columns.values():
            applied_columns.append(filter_name)
    
    # Afficher un résumé des filtres appliqués
    if applied_columns:
        applied_filters_text = []
        for col in applied_columns:
            readable_col = col.replace('_', ' ').title()
            if col in filtered_df.columns:
                unique_values = filtered_df[col].unique()
                if len(unique_values) == 1:
                    value_str = str(unique_values[0])
                    applied_filters_text.append(f"{readable_col}: {value_str}")
                else:
                    applied_filters_text.append(f"{readable_col}: {len(unique_values)} valeurs")
        
        if applied_filters_text:
            filter_summary = html.Div([
                html.Div("Filtres de structure appliqués:", 
                       style={'marginBottom': '8px', 'fontWeight': 'bold', 'fontSize': '14px', 'color': '#000000'}),
                html.Ul([
                    html.Li(text) for text in applied_filters_text
                ], style={'paddingLeft': '20px'})
            ], style={'backgroundColor': '#f5f5f5', 'padding': '15px', 'borderRadius': '5px', 'marginBottom': '20px'})
            
            graphs.append(filter_summary)
    
    # PARTIE 1: GRAPHIQUES SIMPLES DU NOMBRE D'OBSERVATIONS
    # Créer des graphiques simples de distribution pour les colonnes non filtrées
    remaining_columns = [col for label, col in structure_hierarchy 
                         if col not in applied_columns and col in filtered_df.columns]
    
    # Section titre pour les graphiques de distribution
    if remaining_columns:
        graphs.append(html.Div("Distribution du nombre d'observations", style=SECTION_TITLE_STYLE))
    
        for column in remaining_columns:
            # Graphique de distribution simple
            title_prefix = "Nombre d'observations"
            graphs.append(create_bar_chart(filtered_df, column, title_prefix))
    
    # PARTIE 2: GRAPHIQUES DE CROISEMENT OPTIMISÉS
    # Ne prendre que les colonnes non filtrées et disponibles dans le DataFrame
    available_hierarchy = [(label, col) for label, col in structure_hierarchy 
                          if col not in applied_columns and col in filtered_df.columns]
    
    # Créer des croisements entre composants adjacents dans la hiérarchie
    if len(available_hierarchy) >= 2:
        for i in range(len(available_hierarchy) - 1):
            current_label, current_col = available_hierarchy[i]
            next_label, next_col = available_hierarchy[i + 1]
            
            # Titre de section pour chaque paire (en noir)
            graphs.append(html.Div(f"Top 10 des paires {current_label} - {next_label}", style=SECTION_TITLE_STYLE))
            
            try:
                # Calculer le nombre d'observations pour chaque paire (current_col, next_col)
                pair_counts = filtered_df.groupby([current_col, next_col]).size().reset_index(name='count')
                
                # Trier par nombre d'observations décroissant et prendre les 10 premières
                top_pairs = pair_counts.sort_values('count', ascending=False).head(10)
                
                if len(top_pairs) > 0:
                    # Créer des labels pour les paires
                    top_pairs['pair_label'] = top_pairs.apply(
                        lambda row: f"{row[current_col]} - {row[next_col]}", axis=1
                    )
                    
                    # Couleur pour barres horizontales
                    color_scale = [[0, "#003399"], [1, "#e2001a"]]
                    
                    # Créer un graphique à barres horizontales avec largeur optimisée
                    fig = px.bar(
                        top_pairs,
                        y='pair_label',
                        x='count',
                        orientation='h',
                        title=f"Top 10 des paires avec le plus d'observations",
                        labels={
                            'pair_label': f"{current_label} - {next_label}",
                            'count': "Nombre d'observations"
                        },
                        color='count',
                        color_continuous_scale=color_scale,
                        height=max(400, len(top_pairs) * 40)  # Hauteur adaptative
                    )
                    
                    # Configurer la mise en page avec marges élargies pour les longues barres
                    fig.update_layout(
                        margin={"r": 100, "t": 60, "l": 20, "b": 40},  # Augmentation de la marge droite (100px au lieu de 20px)
                        font=GRAPH_FONT,
                        title_font=GRAPH_TITLE_FONT,
                        xaxis_title="Nombre d'observations",
                        yaxis_title=None,
                        plot_bgcolor='white',
                        width=900  # Largeur fixe plus grande (900px) pour tout le graphique
                    )
                    
                    # Ajouter les valeurs sur les barres avec positionnement amélioré
                    max_value = top_pairs['count'].max()  # Valeur maximale pour ajuster le positionnement
                    
                    # Si certaines barres sont très longues, ajuster le positionnement du texte
                    if max_value > 5000:  # Seuil pour les barres longues
                        fig.update_traces(
                            texttemplate='<b>%{x}</b>',
                            textposition='outside',
                            textfont=dict(size=13, color='black'),
                            cliponaxis=False,  # Empêcher que le texte soit coupé
                            hovertemplate='%{y}: %{x} observations<extra></extra>'
                        )
                    else:
                        fig.update_traces(
                            texttemplate='<b>%{x}</b>',
                            textposition='outside',
                            textfont=dict(size=13, color='black'),
                            hovertemplate='%{y}: %{x} observations<extra></extra>'
                        )
                    
                    # Ajouter une grille horizontale pour faciliter la lecture
                    fig.update_yaxes(
                        showgrid=True,
                        gridcolor='rgba(0,0,0,0.05)'
                    )
                    
                    # Étendre l'axe X pour donner plus d'espace pour les valeurs
                    fig.update_xaxes(
                        range=[0, max_value * 1.15]  # Ajouter 15% à la valeur max
                    )
                    
                    # Ajouter une table avec les détails
                    table_header = [
                        html.Thead(html.Tr([
                            html.Th(current_label), 
                            html.Th(next_label), 
                            html.Th("Nb. Observations")
                        ], style={'backgroundColor': '#f0f0f0'}))
                    ]
                    
                    rows = []
                    for i, row in top_pairs.iterrows():
                        rows.append(html.Tr([
                            html.Td(str(row[current_col])),
                            html.Td(str(row[next_col])),
                            html.Td(str(row['count']), style={'fontWeight': 'bold', 'textAlign': 'right'})
                        ]))
                    
                    table_body = [html.Tbody(rows)]
                    
                    try:
                        # Essayer d'utiliser dbc.Table si disponible
                        import dash_bootstrap_components as dbc
                        table = dbc.Table(
                            table_header + table_body,
                            bordered=True,
                            hover=True,
                            striped=True,
                            size="sm",
                            style={'marginTop': '20px'}
                        )
                    except ImportError:
                        # Sinon utiliser la table HTML standard
                        table = html.Table(
                            table_header + table_body,
                            style={
                                'width': '100%',
                                'borderCollapse': 'collapse',
                                'marginTop': '20px'
                            },
                            className='table table-striped table-bordered table-hover'
                        )
                    
                    # Ajouter le graphique et la table dans un même conteneur
                    graphs.append(html.Div([
                        dcc.Graph(
                            figure=fig,
                            config={'displayModeBar': False, 'responsive': True},
                            style={'width': '100%'}  # Assurer que le graphique utilise toute la largeur disponible
                        ),
                        html.Div("Détail des 10 premiers croisements", style=DETAIL_TITLE_STYLE),
                        table
                    ], style={
                        'marginBottom': '30px',
                        'border': '1px solid #ddd',
                        'borderRadius': '8px',
                        'padding': '15px',
                        'backgroundColor': 'white',
                        'boxShadow': '0 2px 5px rgba(0,0,0,0.05)',
                        'width': '100%'  # Utiliser toute la largeur disponible
                    }))
                else:
                    graphs.append(html.Div(
                        f"Aucune paire {current_label}-{next_label} trouvée dans les données filtrées.",
                        style={'color': sfr_colors['dark_grey'], 'fontStyle': 'italic', 'marginBottom': '20px'}
                    ))
            
            except Exception as e:
                print(f"Erreur lors de la création du croisement {current_col}-{next_col}: {e}")
                graphs.append(html.Div(
                    f"Impossible de créer le graphique de croisement entre {current_label} et {next_label}.",
                    style={'color': 'red', 'fontStyle': 'italic', 'marginBottom': '20px'}
                ))
    
    # Si aucun graphique n'a été créé (hormis le résumé des filtres)
    if len(graphs) <= 1:
        graphs.append(html.Div(
            "Toutes les dimensions de structure ont déjà été filtrées. Aucun graphique supplémentaire à générer.",
            style={'color': sfr_colors['dark_grey'], 'fontStyle': 'italic', 'marginBottom': '20px'}
        ))
    
    return graphs

def create_attributes_stats_graphs(filtered_df):
    """
    Crée des graphiques statistiques liés aux attributs techniques
    """
    graphs = []
    
    # Titre principal pour les attributs techniques
    graphs.append(html.Div("Statistiques des attributs techniques", style=SECTION_TITLE_STYLE))
    
    # Graphiques en barre
    if 'olt_model' in filtered_df.columns:
        graphs.append(create_bar_chart(filtered_df, 'olt_model', "Nombre d'observations"))
    
    # Graphiques circulaires pour variables binaires
    binary_columns = {
        'new_boucle': {'title': "Répartition par Nouvelle Boucle"},
        'is_dsp_1': {'title': "Répartition par DSP 1"},
        'code_dep_match': {'title': "Répartition par Match Département-PEAG-OLT", 
                           'mapping': {1: 'Match', 0: 'Pas de match'}}
    }
    
    # Sous-titre pour les variables binaires
    if any(col in filtered_df.columns for col in binary_columns.keys()):
        graphs.append(html.Div("Répartition par variables binaires", style=SUBSECTION_TITLE_STYLE))
    
    for col, options in binary_columns.items():
        if col in filtered_df.columns:
            mapping = options.get('mapping', {1: 'Oui', 0: 'Non'})
            graphs.append(create_pie_chart(filtered_df, col, mapping, options.get('title')))
    
    # Histogramme pour nombre de clients
    if 'nb_client_total' in filtered_df.columns:
        graphs.append(html.Div("Distribution des clients", style=SUBSECTION_TITLE_STYLE))
        
        fig_clients = px.histogram(
            filtered_df,
            x='nb_client_total',
            nbins=20,
            title="Distribution du nombre de clients",
            labels={'nb_client_total': 'Nombre de clients'},
            color_discrete_sequence=["#e2001a"]
        )
        
        fig_clients.update_layout(
            height=400,
            margin={"r": 10, "t": 40, "l": 10, "b": 40},
            font=GRAPH_FONT,
            title_font=GRAPH_TITLE_FONT,
            plot_bgcolor='white'
        )
        
        graphs.append(html.Div([
            dcc.Graph(figure=fig_clients, config={'displayModeBar': False})
        ], style={
            'marginBottom': '20px', 
            'border': '1px solid #ddd', 
            'borderRadius': '8px', 
            'padding': '15px', 
            'backgroundColor': 'white',
            'boxShadow': '0 2px 5px rgba(0,0,0,0.05)',
            'width': '100%'
        }))
    
    return graphs

def create_pie_chart(df, column, mapping={1: 'Oui', 0: 'Non'}, title=None):
    """
    Crée un graphique circulaire générique pour les variables binaires
    """
    readable_column = column.replace('_', ' ').title().replace('Is ', '')
    df_copy = df.copy()
    df_copy[readable_column] = df_copy[column].map(mapping)
    counts = df_copy[readable_column].value_counts().reset_index()
    counts.columns = [readable_column, 'Nombre d\'observations']
    
    chart_title = title or f"Répartition des observations par {readable_column}"
    
    fig = px.pie(
        counts, 
        values='Nombre d\'observations',
        names=readable_column,
        title=chart_title,
        color_discrete_sequence=["#003399", "#e2001a", "#FFA500", "#008000", "#9932CC"]  # Palette plus variée
    )
    
    fig.update_layout(
        height=400,
        margin={"r": 10, "t": 40, "l": 10, "b": 20},
        title_font=GRAPH_TITLE_FONT,
        legend_title_font=dict(size=12, color='#000000'),
        legend_font=dict(size=12, color='#000000')
    )
    
    # Ajouter les pourcentages dans les labels
    fig.update_traces(
        textposition='inside',
        textinfo='percent+label',
        insidetextfont=dict(color='white', size=12),
        hovertemplate='%{label}: %{value} observations<br>%{percent}'
    )
    
    return html.Div([
        dcc.Graph(figure=fig, config={'displayModeBar': False})
    ], style={
        'marginBottom': '20px', 
        'border': '1px solid #ddd', 
        'borderRadius': '8px', 
        'padding': '15px', 
        'backgroundColor': 'white',
        'boxShadow': '0 2px 5px rgba(0,0,0,0.05)',
        'width': '100%'
    })

def create_temporal_stats_graphs(filtered_df):
    """
    Crée des graphiques statistiques liés aux aspects temporels
    """
    graphs = []
    
    # Section titre pour les graphiques temporels
    graphs.append(html.Div("Statistiques temporelles", style=SECTION_TITLE_STYLE))
    
    # Graphique pour jour de la semaine
    if 'day_of_week' in filtered_df.columns:
        day_mapping = {0: 'Lundi', 1: 'Mardi', 2: 'Mercredi', 3: 'Jeudi', 
                      4: 'Vendredi', 5: 'Samedi', 6: 'Dimanche'}
        filtered_df_copy = filtered_df.copy()
        filtered_df_copy['Jour'] = filtered_df_copy['day_of_week'].map(day_mapping)
        
        day_counts = filtered_df_copy['Jour'].value_counts().reset_index()
        day_counts.columns = ['Jour', 'Nombre d\'observations']
        
        # Réordonner les jours correctement
        correct_order = ['Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi', 'Dimanche']
        day_counts['Jour'] = pd.Categorical(day_counts['Jour'], categories=correct_order, ordered=True)
        day_counts = day_counts.sort_values('Jour')
        
        fig_days = px.bar(
            day_counts, 
            x='Jour', 
            y='Nombre d\'observations',
            title="Nombre d'observations par jour de la semaine",
            color='Nombre d\'observations',
            color_continuous_scale=[[0, "#003399"], [1, "#e2001a"]]
        )
        
        fig_days.update_layout(
            height=400, 
            margin={"r": 20, "t": 40, "l": 50, "b": 40},
            font=GRAPH_FONT,
            title_font=GRAPH_TITLE_FONT,
            plot_bgcolor='white'
        )
        
        # Ajouter les valeurs sur les barres
        fig_days.update_traces(
            texttemplate='<b>%{y}</b>',
            textposition='outside',
            textfont=dict(size=13, color='black')
        )
        
        graphs.append(html.Div([
            dcc.Graph(figure=fig_days, config={'displayModeBar': False})
        ], style={
            'marginBottom': '20px', 
            'border': '1px solid #ddd', 
            'borderRadius': '8px', 
            'padding': '15px', 
            'backgroundColor': 'white',
            'boxShadow': '0 2px 5px rgba(0,0,0,0.05)',
            'width': '100%'
        }))
    
    # Graphique pour heure
    if 'heure' in filtered_df.columns:
        hour_counts = filtered_df['heure'].value_counts().reset_index()
        hour_counts.columns = ['Heure', 'Nombre d\'observations']
        hour_counts = hour_counts.sort_values('Heure')
        
        # Créer un graphique à barres plutôt qu'une ligne pour la cohérence
        fig_hours = px.bar(
            hour_counts, 
            x='Heure', 
            y='Nombre d\'observations',
            title="Nombre d'observations par heure",
            color='Nombre d\'observations',
            color_continuous_scale=[[0, "#003399"], [1, "#e2001a"]]
        )
        
        fig_hours.update_layout(
            height=400,
            margin={"r": 20, "t": 40, "l": 50, "b": 40},
            font=GRAPH_FONT,
            title_font=GRAPH_TITLE_FONT,
            plot_bgcolor='white',
            xaxis=dict(
                tickmode='linear', 
                tick0=0, 
                dtick=2,
                title="Heure"
            ),
            yaxis=dict(
                title="Nombre d'observations"
            )
        )
        
        # Ajouter les valeurs sur les barres
        fig_hours.update_traces(
            texttemplate='<b>%{y}</b>',
            textposition='outside',
            textfont=dict(size=13, color='black')
        )
        
        graphs.append(html.Div([
            dcc.Graph(figure=fig_hours, config={'displayModeBar': False})
        ], style={
            'marginBottom': '20px', 
            'border': '1px solid #ddd', 
            'borderRadius': '8px', 
            'padding': '15px', 
            'backgroundColor': 'white',
            'boxShadow': '0 2px 5px rgba(0,0,0,0.05)',
            'width': '100%'
        }))
    
    # Section titre pour les variables binaires
    graphs.append(html.Div("Répartition par variables temporelles binaires", style=SUBSECTION_TITLE_STYLE))
    
    # Graphiques circulaires pour variables temporelles binaires
    temp_binary_columns = {
        'is_weekend': {'title': "Répartition Week-end vs Semaine", 
                       'mapping': {1: 'Week-end', 0: 'Semaine'}},
        'is_peak_hour': {'title': "Répartition par type d'heure", 
                         'mapping': {1: 'Heure de pointe', 0: 'Heure normale'}},
        'is_holiday': {'title': "Répartition par type de jour", 
                        'mapping': {1: 'Jour férié', 0: 'Jour normal'}},
        'is_working_hour': {'title': "Répartition par heure ouvrée/non ouvrée", 
                           'mapping': {1: 'Heure ouvrée', 0: 'Heure non ouvrée'}},
        'is_night_hour': {'title': "Répartition par heure de nuit/jour", 
                          'mapping': {1: 'Heure de nuit', 0: 'Heure de jour'}}
    }
    
    # Organiser les graphiques circulaires en grille de 2 colonnes
    pie_charts = []
    for col, options in temp_binary_columns.items():
        if col in filtered_df.columns:
            pie_charts.append(create_pie_chart(
                filtered_df, col, options['mapping'], options['title']))
    
    # Regrouper les graphiques circulaires par paires
    for i in range(0, len(pie_charts), 2):
        row = []
        row.append(pie_charts[i])
        if i + 1 < len(pie_charts):
            row.append(pie_charts[i + 1])
        
        graphs.append(html.Div(
            row,
            style={'display': 'flex', 'flexWrap': 'wrap', 'gap': '20px', 'justifyContent': 'center'}
        ))
    
    return graphs

def create_france_map_with_department(department_code):
    """
    Crée une carte de la France avec le département sélectionné mis en évidence
    """
    try:
        import requests
        # URL vers un GeoJSON des départements français
        geojson_url = "https://france-geojson.gregoiredavid.fr/repo/departements.geojson"
        
        # Charger les données géoJSON
        response = requests.get(geojson_url)
        departements_geojson = response.json()
        
        # Création d'un DataFrame pour colorer un seul département
        departements_df = pd.DataFrame({
            "code": [f["properties"]["code"] for f in departements_geojson["features"]],
            "value": [1 if f["properties"]["code"] == department_code else 0 for f in departements_geojson["features"]]
        })
        
        # Trouver le nom du département sélectionné
        selected_dept_name = "Département"
        for feature in departements_geojson["features"]:
            if feature["properties"]["code"] == department_code:
                selected_dept_name = feature["properties"]["nom"]
                break
        
        # Créer la carte avec Plotly Express
        fig = px.choropleth(
            departements_df,
            geojson=departements_geojson,
            locations="code",
            featureidkey="properties.code",
            color="value",
            color_continuous_scale=[[0, "#003399"], [1, "#e2001a"]], # Bleu foncé et rouge SFR
            range_color=(0, 1),
            scope="europe"
        )
        
        # Configurer l'apparence
        fig.update_geos(
            fitbounds="locations", 
            visible=False
        )
        
        # Augmenter la taille de la carte
        fig.update_layout(
            title=f"{selected_dept_name} ({department_code})",
            title_font_size=16,
            margin={"r": 5, "t": 40, "l": 5, "b": 5},
            coloraxis_showscale=False,
            height=550,  # Augmentation de la hauteur
            width=500    # Augmentation de la largeur
        )
        
        # Ajouter des bordures blanches pour bien délimiter les départements
        fig.update_traces(
            marker_line_color='white',
            marker_line_width=1
        )
        
        return dcc.Graph(
            figure=fig,
            style={
                'border': '1px solid #ddd', 
                'borderRadius': '5px', 
                'boxShadow': '0 2px 6px rgba(0,0,0,0.1)',
                'marginTop': '10px',
                'marginBottom': '15px'
            },
            config={'displayModeBar': False}
        )
    except Exception as e:
        print(f"Erreur lors de la création de la carte: {e}")
        return html.Div([
            html.P(f"Impossible d'afficher la carte pour le département {department_code}.", 
                   style={'color': '#e2001a'})
        ])