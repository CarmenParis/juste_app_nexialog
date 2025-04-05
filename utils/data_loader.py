# utils/data_loader.py
# Module pour charger et gérer les données parquet

import pandas as pd
from datetime import datetime
import os

class DataManager:
    """
    Classe pour charger et filtrer les données
    """
    _instance = None
    
    @classmethod
    
    def get_instance(cls, parquet_path="donnees.parquet"):
        """Pattern Singleton pour avoir une seule instance"""
        if cls._instance is None:
            cls._instance = DataManager(parquet_path)
        return cls._instance
    
    def __init__(self, parquet_path="donnees.parquet"):
        """Initialise le gestionnaire de données"""
        # Charge les données depuis le fichier parquet
        self.df = pd.read_parquet(parquet_path)
        print(f"Données chargées avec succès: {len(self.df)} lignes")
        
        
        # Conservation d'une copie des données originales
        self.df_original = self.df.copy()
        
        # Mapping des noms d'affichage aux noms de colonnes selon le format donné
        self.column_mapping = dict([
            ("Département", "code_departement"),
            ("DSP 1", "is_dsp_1"),
            ("DSP", "dsp"),
            ("Nouvelle boucle", "new_boucle"),
            ("Boucle", "boucle"),
            ("DEP_PEAG_OLT_match", "code_dep_match"),
            ("Identifiant de PEAG", "peag_nro"),
            ("Modèle d'OLT", "olt_model"),
            ("Identifiant d'OLT", "olt_name"),
            ("PEBIB", "pebib"),
            ("POP DNS", "pop_dns"),
            ("Nombre de clients", "nb_client_total"),
            ("Date", "date"),
            ("Jour de la semaine", "day_of_week"),
            ("Jour férié", "is_holiday"),
            ("Week-end", "is_weekend"),
            ("Heure", "heure"),
            ("Heure de pointe", "is_peak_hour"),
            ("Heure ouvrée", "is_working_hour"),
            ("Heure de nuit", "is_night_hour"),
        ])
        
    def get_filter_options(self, filter_name, current_filters=None):
        """
        Récupère les options disponibles pour un filtre donné
        en tenant compte des filtres déjà appliqués

        Args:
            filter_name (str): Nom du filtre pour lequel récupérer les options
            current_filters (dict, optional): Filtres déjà appliqués

        Returns:
            list: Liste des options disponibles pour le filtre
        """
        # Si aucun filtre n'est passé, utiliser un dictionnaire vide
        if current_filters is None:
            current_filters = {}

        # Appliquer tous les filtres existants sauf celui qu'on est en train de récupérer
        current_filters_without_current = {
            k: v for k, v in current_filters.items() if k != filter_name
        }
        
        # Utiliser filter_dataframe pour obtenir les données déjà filtrées
        filtered_df = self.filter_dataframe(current_filters_without_current)
            
        # Récupérer le nom de colonne pour le filtre demandé
        if filter_name not in self.column_mapping:
            return []
            
        col_name = self.column_mapping[filter_name]
        
        if col_name not in filtered_df.columns:
            return []
            
        # Récupérer les valeurs uniques
        unique_values = filtered_df[col_name].unique()
        
        # Traitements spécifiques selon le type de filtre
        if col_name == 'date':
            dates = pd.to_datetime(unique_values)
            return [dates.min().date(), dates.max().date()]
            
        elif col_name == 'heure':
            return [int(unique_values.min()), int(unique_values.max())]
            
        elif col_name == 'nb_client_total':
            return [float(unique_values.min()), float(unique_values.max())]
            
        # Filtrer les valeurs None
        filtered_values = [val for val in unique_values.tolist() if val is not None]
        return sorted(filtered_values)
        
    def filter_dataframe(self, filters):
        """
        Filtre le dataframe selon les filtres fournis
        
        Args:
            filters: Dictionnaire {nom_filtre: valeur}
            
        Returns:
            DataFrame filtré
        """
        # Partir des données originales
        filtered_df = self.df_original.copy()
        
        # Appliquer chaque filtre
        for filter_name, filter_value in filters.items():
            if filter_name not in self.column_mapping:
                continue
                
            col_name = self.column_mapping[filter_name]
            
            if col_name not in filtered_df.columns:
                continue
                
            # Filtrage selon le type de filtre
            if filter_name == "Date" and isinstance(filter_value, tuple) and len(filter_value) == 2:
                # Convertir en datetime pour le filtrage
                start_date, end_date = pd.to_datetime(filter_value[0]), pd.to_datetime(filter_value[1])
                filtered_df = filtered_df[(pd.to_datetime(filtered_df[col_name]) >= start_date) & 
                                         (pd.to_datetime(filtered_df[col_name]) <= end_date)]
            
            elif filter_name == "Heure" and isinstance(filter_value, tuple) and len(filter_value) == 2:
                min_hour, max_hour = filter_value
                filtered_df = filtered_df[(filtered_df[col_name] >= min_hour) & 
                                         (filtered_df[col_name] <= max_hour)]
            
            elif filter_name == "Jour de la semaine" and isinstance(filter_value, list):
                if filter_value:  # Si des jours sont sélectionnés
                    filtered_df = filtered_df[filtered_df[col_name].isin(filter_value)]
            
            elif filter_name in ["Week-end", "Heure de nuit", "Heure ouvrée", "Jour férié", 
                                "Heure de pointe", "Nouvelle boucle", "DSP 1", "DEP_PEAG_OLT_match"]:
                if filter_value == 'oui':
                    filtered_df = filtered_df[filtered_df[col_name] == 1]
                elif filter_value == 'non':
                    filtered_df = filtered_df[filtered_df[col_name] == 0]
                # Si 'all', ne pas filtrer
            
            elif filter_name == "Nombre de clients" and isinstance(filter_value, tuple) and len(filter_value) == 2:
                min_val, max_val = filter_value
                filtered_df = filtered_df[(filtered_df[col_name] >= min_val) & 
                                         (filtered_df[col_name] <= max_val)]
            
            elif isinstance(filter_value, (str, int, float)) and filter_value:
                # Filtre simple par égalité
                filtered_df = filtered_df[filtered_df[col_name] == filter_value]
                
        return filtered_df
        
    def get_filtered_row_count(self, filters):
        """
        Retourne le nombre de lignes après application des filtres
        """
        filtered_df = self.filter_dataframe(filters)
        return len(filtered_df)