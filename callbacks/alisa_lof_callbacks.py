# callbacks/alisa_lof_callbacks.py
import dash
from dash import html, dcc, callback, Input, Output, State
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
import os

def init_alisa_lof_callbacks(app):
    @app.callback(
        Output('lof-visualization-container', 'children'),
        [Input('lof-filter-values', 'data')],
        prevent_initial_call=True
    )
    def update_lof_visualization(filter_values):
        """
        Met à jour la visualisation des anomalies LOF
        """
        # Vérifier si des filtres ont été sélectionnés
        if not filter_values:
            return [
                html.Div([
                    html.H4("Sélectionnez des filtres et appliquez-les pour visualiser les anomalies", 
                            className="text-center text-muted my-5")
                ])
            ]
        
        # Construire le chemin du fichier CSV
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        csv_path = os.path.join(base_dir, 'lof.csv')
        
        # Charger les données
        try:
            df_detected = pd.read_csv(csv_path, low_memory=False)
        except Exception as e:
            return [
                html.Div([
                    html.H4(f"Erreur de chargement des données: {str(e)}", 
                            className="text-center text-danger my-5")
                ])
            ]
        
        # Créer un timestamp si nécessaire
        if 'timestamp' not in df_detected.columns:
            # Vérifier les colonnes disponibles pour créer le timestamp
            if 'jour' in df_detected.columns and 'heure' in df_detected.columns:
                df_detected['timestamp'] = pd.to_datetime(
                    df_detected['jour'] + ' ' + 
                    df_detected['heure'].astype(str) + ':00:00'
                )
            else:
                return [
                    html.Div([
                        html.H4("Impossible de créer un timestamp", 
                                className="text-center text-danger my-5")
                    ])
                ]
        
        # Créer la colonne chaine_id si elle n'existe pas
        if 'chaine_id' not in df_detected.columns:
            # Vérifier les colonnes nécessaires
            required_cols = ['code_departement', 'peag_nro', 'boucle_simplifiée', 'olt_name']
            if all(col in df_detected.columns for col in required_cols):
                df_detected['chaine_id'] = (
                    df_detected['code_departement'].astype(str) + '_' +
                    df_detected['peag_nro'] + '_' +
                    df_detected['boucle_simplifiée'] + '_' +
                    df_detected['olt_name']
                )
            else:
                return [
                    html.Div([
                        html.H4("Impossible de créer la colonne chaine_id", 
                                className="text-center text-danger my-5")
                    ])
                ]
        
        # Récupérer les valeurs des filtres
        date = filter_values.get('date')
        hour = filter_values.get('hour', 12)
        timeframe = filter_values.get('timeframe', 3)
        lof_threshold = filter_values.get('lof_threshold', '003')
        chain_filter = filter_values.get('chain_filter', 'Toutes')
        indicator_filter = filter_values.get('indicator_filter', 'all')
        
        # Conversion de la date et définition de la période d'analyse
        reference_datetime = pd.to_datetime(f"{date} {hour}:00:00")
        start_time = reference_datetime - pd.Timedelta(hours=timeframe)
        
        # Filtrer les données
        filtered_df = df_detected[
            (df_detected['timestamp'] >= start_time) & 
            (df_detected['timestamp'] <= reference_datetime)
        ].copy()
        
        # Filtrer par chaîne si spécifié (avec gestion du cas 'Toutes')
        if chain_filter != 'Toutes':
            filtered_df = filtered_df[filtered_df['chaine_id'] == chain_filter]
        
        # Vérifier s'il y a des données
        if len(filtered_df) == 0:
            return [
                html.Div([
                    html.H4("Aucune donnée disponible pour les filtres sélectionnés", 
                            className="text-center text-muted my-5")
                ])
            ]
        
        # Colonnes d'anomalies LOF
        anomaly_columns = {
            'dns': f"anomalie_dns_{lof_threshold}",
            'score': f"anomalie_scoring_{lof_threshold}",
            'latency': f"anomalie_latence_{lof_threshold}"
        }
        
        # Créer les colonnes d'anomalies
        for key, col in anomaly_columns.items():
            # Vérifier si la colonne existe, sinon créer une colonne d'anomalies par défaut
            if col in filtered_df.columns:
                filtered_df[f'{key}_lof_anomaly'] = filtered_df[col] == 1
            else:
                filtered_df[f'{key}_lof_anomaly'] = False
        
        # Calculer le nombre total d'anomalies par indicateur
        anomaly_stats = {
            'dns': filtered_df['dns_lof_anomaly'].sum(),
            'score': filtered_df['score_lof_anomaly'].sum(),
            'latency': filtered_df['latency_lof_anomaly'].sum()
        }
        
        # Statistiques générales
        total_observations = len(filtered_df)
        total_anomalies = sum(anomaly_stats.values())
        
        # Composant de statistiques
        stats_component = dbc.Row([
            dbc.Col([
                html.H5(f"{total_observations}", className="text-center display-6"),
                html.P("Observations", className="text-center text-muted")
            ], width=3),
            dbc.Col([
                html.H5(f"{anomaly_stats['dns']}", className="text-center display-6 text-primary"),
                html.P("Anomalies DNS", className="text-center text-muted")
            ], width=3),
            dbc.Col([
                html.H5(f"{anomaly_stats['score']}", className="text-center display-6 text-primary"),
                html.P("Anomalies Score", className="text-center text-muted")
            ], width=3),
            dbc.Col([
                html.H5(f"{anomaly_stats['latency']}", className="text-center display-6 text-primary"),
                html.P("Anomalies Latence", className="text-center text-muted")
            ], width=3)
        ])
        
        # Graphique principal LOF
        fig_lof = _create_lof_figure(
            filtered_df, 
            indicator_filter, 
            lof_threshold
        )
        
        # Ajouter les composants de visualisation
        visualization_components = [
            html.Div([
                dcc.Graph(
                    id='lof-metrics-graph', 
                    figure=fig_lof
                )
            ], className="mt-4 mb-4")
        ]
        
        # Tableau des chaînes critiques
        critical_chains_component = _create_critical_chains_table(filtered_df)
        visualization_components.append(critical_chains_component)
        
        # Assembler tous les composants
        return [stats_component] + visualization_components
    
    def _create_lof_figure(filtered_df, indicator_filter, lof_threshold):
        """
        Crée la figure principale pour les métriques LOF
        """
        # Indicateurs possibles avec valeurs par défaut si colonnes manquantes
        indicators = {
            'dns': {
                'column': 'moy_avg_dns_time' if 'moy_avg_dns_time' in filtered_df.columns else None,
                'anomaly_column': 'dns_lof_anomaly',
                'title': "Temps DNS (ms) - LOF"
            },
            'score': {
                'column': 'moy_avg_score_scoring' if 'moy_avg_score_scoring' in filtered_df.columns else None,
                'anomaly_column': 'score_lof_anomaly',
                'title': "Score Qualité - LOF"
            },
            'latency': {
                'column': 'moy_avg_latence_scoring' if 'moy_avg_latence_scoring' in filtered_df.columns else None,
                'anomaly_column': 'latency_lof_anomaly',
                'title': "Latence (ms) - LOF"
            }
        }
        
        # Filtrer les indicateurs avec données valides
        valid_indicators = {
            k: v for k, v in indicators.items() 
            if v['column'] is not None
        }
        
        # Si aucun indicateur valide, retourner une figure vide
        if not valid_indicators:
            return go.Figure()
        
        # Si tous les indicateurs sont sélectionnés ou aucun indicateur spécifique
        if indicator_filter == 'all' and len(valid_indicators) > 1:
            fig = make_subplots(
                rows=len(valid_indicators), 
                cols=1,
                subplot_titles=[
                    ind_config['title'] for ind_config in valid_indicators.values()
                ],
                shared_xaxes=True,
                vertical_spacing=0.1
            )
            
            # Ajouter les traces pour chaque indicateur
            for i, (ind_key, ind_config) in enumerate(valid_indicators.items(), 1):
                # Points normaux
                fig.add_trace(
                        go.Scatter(
                            x=filtered_df[~filtered_df[ind_config['anomaly_column']]]['timestamp'],
                            y=filtered_df[~filtered_df[ind_config['anomaly_column']]][ind_config['column']],
                            mode='markers',
                            marker=dict(color='blue', size=5),
                            name=f'{ind_config["title"]} (Normal)',
                            text=[f'Valeur: {val:.2f}<br>Chaîne: {chain}' for val, chain in 
                                zip(filtered_df[~filtered_df[ind_config['anomaly_column']]][ind_config['column']], 
                                    filtered_df[~filtered_df[ind_config['anomaly_column']]]['chaine_id'])],
                            hoverinfo='text+x+y'
                        ),
                        row=i, col=1
                    )
                
                # Points d'anomalies
                # Dans la partie où vous créez les traces d'anomalies
                anomalies = filtered_df[filtered_df[ind_config['anomaly_column']]]
                if len(anomalies) > 0:
                    fig.add_trace(
                        go.Scatter(
                            x=anomalies['timestamp'],
                            y=anomalies[ind_config['column']],
                            mode='markers',
                            marker=dict(color='red', size=10, symbol='x'),
                            name=f'{ind_config["title"]} (Anomalie)',
                            text=[f'Valeur: {val:.2f}<br>Chaîne: {chain}' for val, chain in 
                                zip(anomalies[ind_config['column']], anomalies['chaine_id'])],
                            hoverinfo='text+x+y'
                        ),
                        row=i, col=1
                    )
                            
            fig.update_layout(
                height=300 * len(valid_indicators),
                title_text=f"Détection d'anomalies par LOF (Seuil: {lof_threshold})",
                showlegend=True,
                legend=dict(
                    orientation="h",  # Légende horizontale
                    yanchor="bottom", 
                    y=1.2,  # Placer la légende au-dessus du graphique
                    xanchor="right", 
                    x=1
                ),
                margin=dict(t=200),  # Augmenter la marge en haut pour la légende
                plot_bgcolor='white'
            )
        
        # Sinon, créer un graphique pour l'indicateur spécifique
        else:
            # Déterminer l'indicateur à afficher
            if indicator_filter in valid_indicators:
                ind_config = valid_indicators[indicator_filter]
            else:
                # Prendre le premier indicateur valide
                ind_config = list(valid_indicators.values())[0]
            
            fig = go.Figure()
            
            # Points normaux
            fig.add_trace(
                    go.Scatter(
                        x=filtered_df[~filtered_df[ind_config['anomaly_column']]]['timestamp'],
                        y=filtered_df[~filtered_df[ind_config['anomaly_column']]][ind_config['column']],
                        mode='markers',
                        marker=dict(color='blue', size=5),
                        name='Normal',
                        text=[f'Valeur: {val:.2f}<br>Chaîne: {chain}' for val, chain in 
                            zip(filtered_df[~filtered_df[ind_config['anomaly_column']]][ind_config['column']], 
                                filtered_df[~filtered_df[ind_config['anomaly_column']]]['chaine_id'])],
                        hoverinfo='text+x+y'
                    )
                )
            
            # Points d'anomalies
            anomalies = filtered_df[filtered_df[ind_config['anomaly_column']]]
            if len(anomalies) > 0:
                fig.add_trace(
                    go.Scatter(
                        x=anomalies['timestamp'],
                        y=anomalies[ind_config['column']],
                        mode='markers',
                        marker=dict(color='red', size=10, symbol='x'),
                        name='Anomalie',
                        text=[f'Valeur: {val:.2f}<br>Chaîne: {chain}' for val, chain in 
                            zip(anomalies[ind_config['column']], anomalies['chaine_id'])],
                        hoverinfo='text+x+y'
                    )
                )
                        
            fig.update_layout(
                title_text=ind_config['title'],
                height=400,
                showlegend=True,
                legend=dict(
                    orientation="h", 
                    yanchor="bottom", 
                    y=1.1, 
                    xanchor="right", 
                    x=1
                ),
                margin=dict(t=100),
                plot_bgcolor='white'
            )
        
        return fig
    
    def _create_critical_chains_table(filtered_df):
        """
        Crée un tableau des chaînes critiques basé sur anomalies LOF
        """
        # Colonnes d'anomalies
        combined_anomalies = (filtered_df['dns_lof_anomaly'] |
                            filtered_df['score_lof_anomaly'] |
                            filtered_df['latency_lof_anomaly']).sum()
        
        if combined_anomalies > 0:
            # Filtrer les chaînes avec des anomalies
            anomaly_df = filtered_df[
                (filtered_df['dns_lof_anomaly'] |
                filtered_df['score_lof_anomaly'] |
                filtered_df['latency_lof_anomaly'])
            ]
            
            def count_simultaneous_anomalies(group):
                # Compter le nombre d'anomalies détectées simultanément
                return group[['dns_lof_anomaly', 'score_lof_anomaly', 'latency_lof_anomaly']].sum(axis=1).max()
            
            critical_chains = anomaly_df.groupby('chaine_id').apply(lambda x: pd.Series({
                'code_departement': x['code_departement'].iloc[0],
                'peag_nro': x['peag_nro'].iloc[0],
                'boucle_simplifiée': x['boucle_simplifiée'].iloc[0],
                'olt_name': x['olt_name'].iloc[0],
                'dns_lof_anomaly': x['dns_lof_anomaly'].mean(),
                'score_lof_anomaly': x['score_lof_anomaly'].mean(),
                'latency_lof_anomaly': x['latency_lof_anomaly'].mean(),
                'nb_repetitions': len(x),
                'lof_anomaly_count': count_simultaneous_anomalies(x),
                'total_clients': x.get('total_clients', 0).sum() if 'total_clients' in x.columns else 0
            })).reset_index()
            
            # Conversion en pourcentage pour les anomalies par indicateur
            for col in ['dns_lof_anomaly', 'score_lof_anomaly', 'latency_lof_anomaly']:
                critical_chains[col] = critical_chains[col] * 100
            
            # Classification de sévérité
            conditions = [
                (critical_chains['total_clients'] > 100) & (critical_chains['lof_anomaly_count'] > 1) & (critical_chains['nb_repetitions'] > 1),
                (critical_chains['total_clients'] > 50) & (critical_chains['lof_anomaly_count'] > 1),
                (critical_chains['total_clients'] > 50) & (critical_chains['lof_anomaly_count'] > 0)
            ]
            choices = ['Grave', 'Élevé', 'Moyen']
            critical_chains['severity'] = np.select(conditions, choices, default='Faible')
            
            # Mapper les sévérités à des valeurs pour le tri
            severity_map = {'Grave': 4, 'Élevé': 3, 'Moyen': 2, 'Faible': 1}
            critical_chains['severity_value'] = critical_chains['severity'].map(severity_map)
            
            # Trier par sévérité et nombre de clients
            critical_chains = critical_chains.sort_values(['severity_value', 'total_clients'], ascending=[False, False])
            
            # Création du tableau HTML
            table = html.Table([
                html.Thead(
                    html.Tr([
                        html.Th("Département"),
                        html.Th("PEAG/NRO"),
                        html.Th("Boucle"),
                        html.Th("OLT"),
                        html.Th("Sévérité"),
                        html.Th("Nb Répétitions"),
                        html.Th(["Nb Indicateurs", html.Br(), html.Small("(en même temps)")]),
                        html.Th("DNS LOF (%)"),
                        html.Th("Score LOF (%)"),
                        html.Th("Latence LOF (%)"),
                        html.Th("Clients")
                    ])
                ),
                html.Tbody([
                    html.Tr([
                        html.Td(row['code_departement']),
                        html.Td(row['peag_nro']),
                        html.Td(row['boucle_simplifiée']),
                        html.Td(row['olt_name']),
                        html.Td(row['severity'], 
                                style={
                                    'background-color': (
                                        'darkred' if row['severity'] == 'Grave' else
                                        'red' if row['severity'] == 'Élevé' else
                                        'yellow' if row['severity'] == 'Moyen' else
                                        'blue' if row['severity'] == 'Faible' else
                                        'white'
                                    ),
                                    'color': 'white' if row['severity'] in ['Grave', 'Élevé'] else 'black'
                                }),
                        html.Td(int(row['nb_repetitions'])),
                        html.Td(int(row['lof_anomaly_count'])),
                        html.Td(f"{row['dns_lof_anomaly']:.1f}%"),
                        html.Td(f"{row['score_lof_anomaly']:.1f}%"),
                        html.Td(f"{row['latency_lof_anomaly']:.1f}%"),
                        html.Td(f"{int(row['total_clients'])}" if row['total_clients'] > 0 else "N/A",
                                style={'font-weight': 'bold'} if row['total_clients'] > 100 else {})
                    ]) for i, row in critical_chains.head(50).iterrows()
                ])
            ], className="table table-striped table-hover")
            
            # Description de la sévérité
            severity_description = html.Div([
                html.H5("Classification de sévérité:", className="mb-2 mt-3"),
                html.Ul([
                    html.Li([html.Span("Grave: ", style={'font-weight': 'bold', 'color': 'darkred'}), 
                            "Client > 100, indicateur > 1 et répétition > 1"]),
                    html.Li([html.Span("Élevé: ", style={'font-weight': 'bold', 'color': 'red'}), 
                            "Client > 50 et indicateur > 1"]),
                    html.Li([html.Span("Moyen: ", style={'font-weight': 'bold', 'color': 'orange'}), 
                            "Client > 50 avec au moins une anomalie détectée"]),
                    html.Li([html.Span("Faible: ", style={'font-weight': 'bold', 'color': 'blue'}), 
                            "Anomalie isolée"])
                ], className="mb-3")
            ])
            
            table_component = html.Div([
                html.P(f"Top 50 chaînes critiques sur {len(critical_chains)} chaînes avec anomalies:"),
                severity_description,
                table
            ])
        else:
            table_component = html.P("Aucune anomalie détectée dans la période sélectionnée.")
        
        return table_component
    