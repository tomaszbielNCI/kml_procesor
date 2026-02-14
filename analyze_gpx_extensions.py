import pandas as pd
import xml.etree.ElementTree as ET

# Odczytaj plik backup
backup_file = 'data/input/full_backup_13_Feb_2026_00_15_38.gpx'

print('=== DOKLADNA ANALIZA ROZSZERZEN GPX ===')

try:
    # Parsuj GPX
    tree = ET.parse(backup_file)
    root = tree.getroot()
    
    # Znajdź pierwszą trasę z punktami
    tracks = root.findall('.//{http://www.topografix.com/GPX/1/1}trk')
    
    for i, track in enumerate(tracks):
        name_elem = track.find('.//{http://www.topografix.com/GPX/1/1}name')
        track_name = name_elem.text if name_elem is not None else 'No name'
        
        # Znajdź wszystkie punkty w trasie
        track_points = track.findall('.//{http://www.topografix.com/GPX/1/1}trkpt')
        
        if len(track_points) > 0:
            print(f'\n=== TRASA {i+1}: {track_name} ===')
            print(f'Liczba punktów: {len(track_points)}')
            
            # Sprawdź pierwsze 3 punkty dokładnie
            for j, point in enumerate(track_points[:3]):
                print(f'\nPunkt {j+1}:')
                
                # Podstawowe dane
                lat = point.get('lat')
                lon = point.get('lon')
                print(f'  Współrzędne: {lat}, {lon}')
                
                # Elewacja
                ele_elem = point.find('.//{http://www.topografix.com/GPX/1/1}ele')
                if ele_elem is not None:
                    print(f'  Elewacja: {ele_elem.text}')
                
                # Rozszerzenia - pełna analiza
                extensions = point.find('.//{http://www.topografix.com/GPX/1/1}extensions')
                if extensions is not None:
                    print('  Rozszerzenia znalezione:')
                    
                    # Przejdź przez wszystkie elementy w rozszerzeniach
                    for elem in extensions.iter():
                        if elem.tag:
                            tag_name = elem.tag.split('}')[-1] if '}' in elem.tag else elem.tag
                            print(f'    Tag: {tag_name}')
                            
                            # Wypisz wszystkie atrybuty
                            for attr_name, attr_value in elem.attrib.items():
                                print(f'      {attr_name}: {attr_value}')
                            
                            # Wypisz tekst jeśli istnieje
                            if elem.text and elem.text.strip():
                                print(f'      Text: {elem.text.strip()}')
                else:
                    print('  Brak rozszerzeń')
            
            # Sprawdź kilka punktów z końca i środka
            check_indices = []
            if len(track_points) > 10:
                check_indices.append(len(track_points) // 2)  # Środek
                check_indices.append(len(track_points) - 2)    # Przedostatni
            
            for idx in check_indices:
                if idx < len(track_points):
                    point = track_points[idx]
                    print(f'\nPunkt {idx+1} (środek/koniec):')
                    
                    extensions = point.find('.//{http://www.topografix.com/GPX/1/1}extensions')
                    if extensions is not None:
                        for elem in extensions.iter():
                            if elem.tag:
                                tag_name = elem.tag.split('}')[-1] if '}' in elem.tag else elem.tag
                                if 'clock' in tag_name.lower() or 'seconds' in tag_name.lower() or 'time' in tag_name.lower():
                                    print(f'  CZAS: {tag_name}')
                                    for attr_name, attr_value in elem.attrib.items():
                                        print(f'    {attr_name}: {attr_value}')
                    else:
                        print('  Brak rozszerzeń w tym punkcie')
            
            break  # Tylko pierwsza trasa z punktami
            
except Exception as e:
    print(f'Błąd: {e}')
    import traceback
    traceback.print_exc()
