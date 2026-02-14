#!/usr/bin/env python3
"""
Snippet do analizy danych GPX z kaloriami i metadanymi
"""

import os
import sys
import pandas as pd
import gpxpy
from xml.etree import ElementTree as ET

# Dodanie ścieżki do core
sys.path.append(os.path.join(os.path.dirname(__file__), 'core'))

def analyze_gpx_with_calories(gpx_file_path):
    """Analiza pliku GPX z danymi o kaloriach i innych metadanych"""
    
    print(f"=== Analiza pliku: {os.path.basename(gpx_file_path)} ===\n")
    
    # Wczytanie pliku GPX
    with open(gpx_file_path, 'r', encoding='utf-8') as f:
        gpx_content = f.read()
    
    # Parsowanie GPX
    gpx = gpxpy.parse(gpx_content)
    
    # Analiza XML dla dodatkowych danych
    root = ET.fromstring(gpx_content)
    
    # Zbieranie danych z rozszerzeń
    track_data = []
    
    for track_idx, track in enumerate(gpx.tracks):
        print(f"Trasa {track_idx + 1}: {track.name}")
        
        # Pobranie opisu z metadanych
        if track.description:
            print(f"   Opis: {track.description}")
        
        for segment_idx, segment in enumerate(track.segments):
            for point_idx, point in enumerate(segment.points):
                # Dodatkowe dane z rozszerzeń
                extensions_data = {}
                
                # Szukanie rozszerzeń w XML
                for trkpt in root.findall('.//{http://www.topografix.com/GPX/1/1}trkpt'):
                    if float(trkpt.get('lat')) == point.latitude and float(trkpt.get('lon')) == point.longitude:
                        ext = trkpt.find('.//{http://www.garmin.com/xmlschemas/TrackPointExtension/v1}TrackPointExtension')
                        if ext is not None:
                            for child in ext:
                                tag_name = child.tag.split('}')[-1]  # Usunięcie namespace
                                extensions_data[tag_name] = child.text
                
                track_data.append({
                    'track_name': track.name if track.name else f"Track_{track_idx + 1}",
                    'latitude': point.latitude,
                    'longitude': point.longitude,
                    'altitude': point.elevation if point.elevation else 0.0,
                    'time': point.time.isoformat() if point.time else None,
                    'speed': extensions_data.get('speed'),
                    'calories': extensions_data.get('calories'),
                    'distance': extensions_data.get('distance'),
                    'clock': extensions_data.get('clock'),
                    'seconds': extensions_data.get('seconds'),
                    'source_file': os.path.basename(gpx_file_path)
                })
                
                # Wyświetl pierwsze 5 punktów dla podglądu
                if point_idx < 5:
                    print(f"   Punkt {point_idx + 1}: lat={point.latitude:.6f}, lon={point.longitude:.6f}, alt={point.elevation:.1f}m")
                    if extensions_data.get('calories'):
                        print(f"      Kalorie: {extensions_data.get('calories')} kcal")
                    if extensions_data.get('speed'):
                        print(f"      Predkosc: {extensions_data.get('speed')} m/s")
    
    # Tworzenie DataFrame
    df = pd.DataFrame(track_data)
    
    if not df.empty:
        print(f"\nStatystyki DataFrame:")
        print(f"   • Liczba punktów: {len(df)}")
        print(f"   • Liczba tras: {df['track_name'].nunique()}")
        print(f"   • Zakres wysokosci: {df['altitude'].min():.1f} - {df['altitude'].max():.1f} m")
        
        # Konwersja kolumn numerycznych
        numeric_cols = ['speed', 'calories', 'distance', 'seconds']
        for col in numeric_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')
        
        # Statystyki kalorii
        if 'calories' in df.columns and df['calories'].notna().any():
            print(f"   • Zakres kalorii: {df['calories'].min():.1f} - {df['calories'].max():.1f} kcal")
            print(f"   • Srednie kalorie: {df['calories'].mean():.1f} kcal")
        
        # Statystyki prędkości
        if 'speed' in df.columns and df['speed'].notna().any():
            print(f"   • Zakres predkosci: {df['speed'].min():.2f} - {df['speed'].max():.2f} m/s")
            print(f"   • Srednia predkosc: {df['speed'].mean():.2f} m/s")
        
        print(f"\nKolumny DataFrame: {list(df.columns)}")
        
        # Wyświetlenie pierwszych wierszy
        print(f"\nPierwsze 10 wierszy DataFrame:")
        print(df.head(10).to_string())
        
        # Wyświetlenie typów danych
        print(f"\nTypy danych:")
        print(df.dtypes)
        
    else:
        print("Nie znaleziono danych w pliku GPX")
    
    return df

# Przykład użycia
if __name__ == "__main__":
    # Ścieżka do przykładowego pliku GPX
    gpx_file = "../data/input/full_backup_1_Jun_2025_10_24_46.gpx"
    
    if os.path.exists(gpx_file):
        df = analyze_gpx_with_calories(gpx_file)
        
        # Opcjonalnie: zapis do CSV
        if not df.empty:
            output_csv = "data/output/gpx_analysis_sample.csv"
            df.to_csv(output_csv, index=False)
            print(f"\nZapisano analize do: {output_csv}")
    else:
        print(f"Plik nie istnieje: {gpx_file}")
        print("Dostepne pliki GPX:")
        input_dir = "../data/input"
        if os.path.exists(input_dir):
            gpx_files = [f for f in os.listdir(input_dir) if f.endswith('.gpx')]
            for f in gpx_files[:5]:  # Pokaż pierwsze 5
                print(f"   • {f}")
