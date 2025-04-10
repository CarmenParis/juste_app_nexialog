# callbacks/isolation_forest_callbacks.py
# Callbacks pour la page de détection d'anomalies avec Isolation Forest

from dash import html, dcc, callback, Input, Output, State
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
import os
from datetime import datetime, timedelta
import dash

# Fonction pour charger les données d'anomalies à partir des fichiers CSV
def load_anomaly_data(contamination=0.005, olt_name=None, date_range=None, hour_range=None):
    """
    Charge les données d'anomalies à partir des fichiers CSV selon le niveau de contamination
    
    Args:
        contamination: Le niveau de contamination (0.001, 0.005, 0.01)
        olt_name: L'identifiant de l'OLT à filtrer (ou None pour tous)
        date_range: Liste des dates au format "YYYY-MM-DD" à inclure
        hour_range: La plage horaire à filtrer [min, max]
        
    Returns:
        DataFrame contenant les données d'anomalies
    """
    # Construire le chemin du fichier en fonction du niveau de contamination
    file_path = f"output/df_agg_with_anomalies_contam_{contamination}.csv"
    
    try:
        # Vérifier si le fichier existe
        if not os.path.exists(file_path):
            print(f"Le fichier {file_path} n'existe pas.")
            return pd.DataFrame()  # Retourner un DataFrame vide
        
        # Charger le fichier CSV
        # Format attendu: hour,olt_name,dns_flag,scoring_flag,date_hour,date,grave_anomalies
        df = pd.read_csv(file_path)
        
        print(f"Colonnes dans le fichier CSV: {df.columns.tolist()}")
        print(f"Exemples de dates dans le CSV: {df['date'].head(3).tolist() if 'date' in df.columns else 'No date column'}")
        
        # Convertir certaines colonnes pour faciliter le filtrage
        if 'date_hour' in df.columns:
            df['date_hour'] = pd.to_datetime(df['date_hour'])
            # Extraire l'heure si la colonne hour n'existe pas
            if 'hour' not in df.columns:
                df['hour'] = df['date_hour'].dt.hour
        
        if 'date' in df.columns:
            # S'assurer que la colonne date est au format datetime
            df['date'] = pd.to_datetime(df['date'])
            # Créer une colonne de date au format string YYYY-MM-DD pour le filtrage
            df['date_str'] = df['date'].dt.strftime('%Y-%m-%d')
        
        # Créer une colonne is_anomaly basée sur grave_anomalies
        if 'grave_anomalies' in df.columns:
            df['is_anomaly'] = df['grave_anomalies'] > 0
        
        # Appliquer les filtres
        if olt_name:
            df = df[df['olt_name'] == olt_name]
        
        if date_range and len(date_range) > 0:
            try:
                if 'date_str' in df.columns:
                    df = df[df['date_str'].isin(date_range)]
                elif 'date' in df.columns:
                    # Créer des objets datetime pour la plage de dates
                    date_range_dt = [pd.to_datetime(d) for d in date_range]
                    df = df[df['date'].dt.date.isin([d.date() for d in date_range_dt])]
            except Exception as e:
                print(f"Erreur lors du filtrage par dates: {e}")
        
        if hour_range and len(hour_range) == 2:
            try:
                min_hour, max_hour = int(hour_range[0]), int(hour_range[1])
                if 'hour' in df.columns:
                    df = df[(df['hour'] >= min_hour) & (df['hour'] <= max_hour)]
            except (ValueError, TypeError) as e:
                print(f"Erreur lors du filtrage par heures: {e}")
        
        print(f"Données chargées à partir de {file_path} avec succès. {len(df)} lignes après filtrage.")
        
        if df.empty:
            print("Attention: DataFrame vide après application des filtres.")
        
        return df
    
    except Exception as e:
        print(f"Erreur lors du chargement du fichier {file_path}: {e}")
        return pd.DataFrame()  # Retourner un DataFrame vide en cas d'erreur

# Cette fonction sera appelée depuis app.py
def init_isolation_forest_callbacks(app):
    """
    Initialise les callbacks pour la page de détection d'anomalies
    
    Args:
        app: L'application Dash
    """
    
    @app.callback(
        Output("anomaly-visualization-container", "children"),
        Input("isolation-forest-filter-values", "data")
    )
    def update_anomaly_visualization(filter_values):
        if not filter_values:
            # Afficher un message par défaut si aucun filtre n'est appliqué
            return html.Div([
                html.H4("Sélectionnez des filtres et appliquez-les pour visualiser les anomalies", 
                        className="text-center text-muted my-5")
            ])
        
        # Extraire les valeurs des filtres
        olt_value = filter_values.get("olt_name")
        date_range = filter_values.get("date_range", [])
        hour_range = filter_values.get("hour", [0, 23])
        contamination = filter_values.get("contamination", 0.005)  # Valeur par défaut si non spécifiée
        
        # Afficher les informations de filtrage
        start_date = filter_values.get("start_date")
        end_date = filter_values.get("end_date")
        date_info = f"du {start_date} au {end_date}" if start_date and end_date else "aucune"
        
        print(f"Filtres appliqués: OLT={olt_value}, Période={date_info}, Heures={hour_range}, Contamination={contamination}")
        
        # Charger les données selon le niveau de contamination et les filtres
        df = load_anomaly_data(contamination, olt_value, date_range, hour_range)
        
        # Vérifier si le DataFrame est vide
        if df.empty:
            return html.Div([
                html.H4("Aucune donnée disponible pour les filtres sélectionnés", 
                        className="text-center text-muted my-5")
            ])
        
        # Extraire les anomalies
        anomalies_df = df[df['is_anomaly']] if 'is_anomaly' in df.columns else pd.DataFrame()
        
        # Créer la figure du graphique principal en fonction des colonnes disponibles
        fig_main = go.Figure()
        
        # Utiliser dns_flag comme valeur principale par défaut si disponible
        value_column = 'dns_flag' if 'dns_flag' in df.columns else 'grave_anomalies'
        
        # Si plusieurs jours sont sélectionnés, regrouper par date et heure
        if len(date_range) > 1:
            # Créer une colonne date_hour pour l'axe X
            if 'date' in df.columns and 'hour' in df.columns:
                df['date_hour_str'] = df['date'].dt.strftime('%Y-%m-%d') + ' ' + df['hour'].astype(str) + 'h'
                
                # Regrouper les données par date et heure
                grouped_df = df.groupby(['date_str', 'hour']).agg({
                    value_column: 'mean',
                    'is_anomaly': 'sum'
                }).reset_index()
                
                # Trier par date et heure
                grouped_df['date_hour'] = pd.to_datetime(grouped_df['date_str']) + pd.to_timedelta(grouped_df['hour'], unit='h')
                grouped_df = grouped_df.sort_values('date_hour')
                
                # Créer des étiquettes pour l'axe X
                x_labels = [f"{d} {h}h" for d, h in zip(grouped_df['date_str'], grouped_df['hour'])]
                
                # Ajouter la ligne des valeurs normales
                fig_main.add_trace(go.Scatter(
                    x=x_labels,
                    y=grouped_df[value_column],
                    mode='lines+markers',
                    name='Valeurs',
                    line=dict(color='blue', width=2),
                    marker=dict(size=8)
                ))
                
                # Ajouter les points d'anomalies
                anomaly_points = grouped_df[grouped_df['is_anomaly'] > 0]
                if not anomaly_points.empty:
                    anomaly_labels = [f"{d} {h}h" for d, h in zip(anomaly_points['date_str'], anomaly_points['hour'])]
                    fig_main.add_trace(go.Scatter(
                        x=anomaly_labels,
                        y=anomaly_points[value_column],
                        mode='markers',
                        name='Anomalies',
                        marker=dict(color='red', size=12, symbol='circle-open')
                    ))
            else:
                # Fallback si les colonnes nécessaires ne sont pas disponibles
                fig_main.add_trace(go.Scatter(
                    x=df.index,
                    y=df[value_column],
                    mode='lines+markers',
                    name='Valeurs'
                ))
        else:
            # Pour un seul jour, regrouper simplement par heure
            hour_groups = df.groupby('hour')
            hour_data = hour_groups.agg({
                value_column: 'mean',
                'is_anomaly': 'sum'
            }).reset_index()
            
            # Ajouter la ligne des valeurs normales
            fig_main.add_trace(go.Scatter(
                x=hour_data['hour'],
                y=hour_data[value_column],
                mode='lines+markers',
                name='Valeurs',
                line=dict(color='blue', width=2),
                marker=dict(size=8)
            ))
            
            # Ajouter les points d'anomalies
            anomaly_hours = hour_data[hour_data['is_anomaly'] > 0]
            if not anomaly_hours.empty:
                fig_main.add_trace(go.Scatter(
                    x=anomaly_hours['hour'],
                    y=anomaly_hours[value_column],
                    mode='markers',
                    name='Anomalies',
                    marker=dict(color='red', size=12, symbol='circle-open')
                ))
        
        # Mise en page du graphique principal
        title = "Détection d'anomalies avec Isolation Forest"
        if olt_value:
            title += f" - OLT: {olt_value}"
        if start_date and end_date:
            if start_date == end_date:
                title += f" - Date: {start_date}"
            else:
                title += f" - Période: {start_date} à {end_date}"
        title += f" - Contamination: {contamination}"
            
        fig_main.update_layout(
            title=title,
            xaxis_title="Période" if len(date_range) > 1 else "Heure",
            yaxis_title=value_column,
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            hovermode="closest",
            plot_bgcolor="white",
            height=400
        )
        
        # Si plusieurs jours sont sélectionnés, ajuster l'axe X
        if len(date_range) > 1:
            fig_main.update_layout(
                xaxis=dict(
                    tickangle=45,
                    tickmode='array',
                    tickvals=list(range(len(x_labels))),
                    ticktext=x_labels
                )
            )
        
        # Créer un graphique pour la distribution des anomalies
        if len(date_range) > 1:
            # Distribution des anomalies par jour
            anomaly_dist = df.groupby('date_str')['is_anomaly'].sum().reset_index()
            anomaly_dist.columns = ['date', 'anomaly_count']
            
            fig_anomaly_dist = px.bar(
                anomaly_dist,
                x='date',
                y='anomaly_count',
                title=f"Distribution des anomalies par jour (contamination: {contamination})",
                labels={'date': 'Date', 'anomaly_count': 'Nombre d\'anomalies'},
                color_discrete_sequence=['salmon']
            )
            fig_anomaly_dist.update_layout(
                xaxis=dict(tickangle=45),
                plot_bgcolor="white",
                height=300
            )
        else:
            # Distribution des anomalies par heure
            anomaly_dist = df.groupby('hour')['is_anomaly'].sum().reset_index()
            anomaly_dist.columns = ['hour', 'anomaly_count']
            
            fig_anomaly_dist = px.bar(
                anomaly_dist,
                x='hour',
                y='anomaly_count',
                title=f"Distribution des anomalies par heure (contamination: {contamination})",
                labels={'hour': 'Heure', 'anomaly_count': 'Nombre d\'anomalies'},
                color_discrete_sequence=['salmon']
            )
            fig_anomaly_dist.update_layout(
                xaxis=dict(tickmode='linear', tick0=0, dtick=1),
                plot_bgcolor="white",
                height=300
            )
        
        # Calculer quelques statistiques
        anomaly_count = int(df['is_anomaly'].sum())
        grave_anomalies_avg = anomalies_df['grave_anomalies'].mean() if not anomalies_df.empty and 'grave_anomalies' in anomalies_df.columns else 0
        
        # Créer le contenu de la visualisation
        content = [
            # Statistiques d'anomalies (Le graphique "Trafic réseau et anomalies détectées" a été supprimé)
            dbc.Card([
                dbc.CardHeader("Statistiques d'anomalies"),
                dbc.CardBody([
                    dbc.Row([
                        dbc.Col([
                            html.H5("Nombre d'anomalies"),
                            html.H2(f"{anomaly_count}", className="text-danger")
                        ], width=4),
                        dbc.Col([
                            html.H5("Score moyen des anomalies"),
                            html.H2(f"{grave_anomalies_avg:.2f}" if grave_anomalies_avg > 0 else "N/A", 
                                   className="text-warning")
                        ], width=4),
                        dbc.Col([
                            html.H5("Contamination"),
                            html.H2(f"{contamination}", className="text-info")
                        ], width=4)
                    ]),
                    html.Hr(),
                    dcc.Graph(
                        id="anomaly-dist-graph",
                        figure=fig_anomaly_dist,
                        config={'displayModeBar': False}
                    )
                ])
            ], className="mb-4")]
        
        # Ajouter des graphiques supplémentaires pour dns_flag et scoring_flag si disponibles
        if 'dns_flag' in df.columns and 'scoring_flag' in df.columns:
            flags_row = dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            dcc.Graph(
                                id="dns-flag-graph",
                                figure=create_flag_figure(df, 'dns_flag', 'DNS Flag', 'green', date_range),
                                config={'displayModeBar': False}
                            )
                        ])
                    ])
                ], width=6),
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            dcc.Graph(
                                id="scoring-flag-graph",
                                figure=create_flag_figure(df, 'scoring_flag', 'Scoring Flag', 'purple', date_range),
                                config={'displayModeBar': False}
                            )
                        ])
                    ])
                ], width=6)
            ], className="mb-4")
            content.append(html.H4("Métriques détaillées", className="mt-4 mb-3"))
            content.append(flags_row)
        
        # Tableau des anomalies détectées (si des anomalies existent)
        if not anomalies_df.empty:
            # Sélectionner les colonnes disponibles pour l'affichage
            display_cols = [col for col in ['date_str', 'hour', 'olt_name', 'dns_flag', 'scoring_flag', 'grave_anomalies'] 
                           if col in anomalies_df.columns]
            
            # Créer un DataFrame pour l'affichage avec des noms de colonnes lisibles
            column_mapping = {
                'date_str': 'Date',
                'hour': 'Heure', 
                'olt_name': 'OLT',
                'dns_flag': 'DNS Flag',
                'scoring_flag': 'Scoring Flag',
                'grave_anomalies': 'Score d\'anomalie'
            }
            
            display_df = anomalies_df[display_cols].rename(columns={
                col: column_mapping[col] for col in display_cols if col in column_mapping
            })
            
            if 'Score d\'anomalie' in display_df.columns:
                display_df = display_df.sort_values(by='Score d\'anomalie', ascending=False)
            
            content.append(html.H4("Détails des anomalies détectées", className="mt-4 mb-3"))
            content.append(
                dbc.Card([
                    dbc.CardBody([
                        dbc.Table.from_dataframe(
                            display_df,
                            striped=True,
                            bordered=True,
                            hover=True,
                            responsive=True
                        )
                    ])
                ])
            )
        
        return content

# Fonction pour créer un graphique de flag (dns_flag ou scoring_flag)
def create_flag_figure(df, flag_column, title, color, date_range=None):
    """
    Crée un graphique pour un flag spécifique
    
    Args:
        df: DataFrame contenant les données
        flag_column: Nom de la colonne du flag
        title: Titre du graphique
        color: Couleur de la ligne
        date_range: Liste des dates sélectionnées (pour déterminer le mode de regroupement)
        
    Returns:
        Figure Plotly
    """
    fig = go.Figure()
    
    # Si plusieurs jours sont sélectionnés, regrouper par jour et heure
    if date_range and len(date_range) > 1:
        # Regrouper par date et heure
        grouped_df = df.groupby(['date_str', 'hour']).agg({
            flag_column: 'mean',
            'is_anomaly': 'sum'
        }).reset_index()
        
        # Trier par date et heure
        grouped_df['date_hour'] = pd.to_datetime(grouped_df['date_str']) + pd.to_timedelta(grouped_df['hour'], unit='h')
        grouped_df = grouped_df.sort_values('date_hour')
        
        # Créer des étiquettes pour l'axe X
        x_labels = [f"{d} {h}h" for d, h in zip(grouped_df['date_str'], grouped_df['hour'])]
        
        # Ajouter la ligne du flag
        fig.add_trace(go.Scatter(
            x=x_labels,
            y=grouped_df[flag_column],
            mode='lines',
            name=title,
            line=dict(color=color, width=2)
        ))
        
        # Ajouter les points d'anomalies
        anomaly_points = grouped_df[grouped_df['is_anomaly'] > 0]
        if not anomaly_points.empty:
            anomaly_labels = [f"{d} {h}h" for d, h in zip(anomaly_points['date_str'], anomaly_points['hour'])]
            fig.add_trace(go.Scatter(
                x=anomaly_labels,
                y=anomaly_points[flag_column],
                mode='markers',
                name='Anomalies',
                marker=dict(color='red', size=10)
            ))
        
        fig.update_layout(
            title=title,
            xaxis_title="Période",
            yaxis_title="Valeur",
            xaxis=dict(
                tickangle=45,
                tickmode='array',
                tickvals=list(range(len(x_labels))),
                ticktext=x_labels
            ),
            plot_bgcolor="white",
            height=250
        )
    else:
        # Pour un seul jour, regrouper simplement par heure
        hour_groups = df.groupby('hour')
        hour_data = hour_groups.agg({
            flag_column: 'mean',
            'is_anomaly': 'sum'
        }).reset_index()
        
        # Ajouter la ligne du flag
        fig.add_trace(go.Scatter(
            x=hour_data['hour'],
            y=hour_data[flag_column],
            mode='lines',
            name=title,
            line=dict(color=color, width=2)
        ))
        
        # Ajouter les points d'anomalies
        anomaly_hours = hour_data[hour_data['is_anomaly'] > 0]
        if not anomaly_hours.empty:
            fig.add_trace(go.Scatter(
                x=anomaly_hours['hour'],
                y=anomaly_hours[flag_column],
                mode='markers',
                name='Anomalies',
                marker=dict(color='red', size=10)
            ))
        
        fig.update_layout(
            title=title,
            xaxis_title="Heure",
            yaxis_title="Valeur",
            xaxis=dict(tickmode='linear', tick0=0, dtick=2),
            plot_bgcolor="white",
            height=250
        )
    
    return fig