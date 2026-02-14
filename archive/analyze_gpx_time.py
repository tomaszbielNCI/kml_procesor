import pandas as pd
import xml.etree.ElementTree as ET

# Odczytaj plik backup
backup_file = 'data/input/full_backup_13_Feb_2026_00_15_38.gpx'

print('=== ANALIZA CZASU W PLIKU GPX BACKUP ===')

try:
    # Parsuj GPX
    tree = ET.parse(backup_file)
    root = tree.getroot()
    
    # Znajdź wszystkie trasy
    tracks = root.findall('.//{http://www.topografix.com/GPX/1/1}trk')
    print(f'Liczba tras w pliku: {len(tracks)}')
    
    for i, track in enumerate(tracks[:3]):  # Pierwsze 3 trasy
        name_elem = track.find('.//{http://www.topografix.com/GPX/1/1}name')
        track_name = name_elem.text if name_elem is not None else 'No name'
        
        print(f'\nTrasa {i+1}: {track_name}')
        
        # Znajdź wszystkie punkty w trasie
        track_points = track.findall('.//{http://www.topografix.com/GPX/1/1}trkpt')
        print(f'  Punkty w trasie: {len(track_points)}')
        
        # Sprawdź pierwsze 5 punktów pod kątem czasu
        print('  Pierwsze 5 punktów:')
        for j, point in enumerate(track_points[:5]):
            lat = point.get('lat')
            lon = point.get('lon')
            ele_elem = point.find('.//{http://www.topografix.com/GPX/1/1}ele')
            alt = ele_elem.text if ele_elem is not None else 'No altitude'
            
            # Szukaj czasu w rozszerzeniach
            time_found = False
            extensions = point.find('.//{http://www.topografix.com/GPX/1/1}extensions')
            if extensions is not None:
                # Szukaj różnych elementów czasu
                time_elems = extensions.findall('.//*[@clock]')
                if time_elems:
                    for time_elem in time_elems:
                        print(f'    Punkt {j+1}: {lat}, {lon}, alt={alt}, clock={time_elem.get("clock")}')
                        time_found = True
                        break
                
                # Szukaj seconds
                if not time_found:
                    seconds_elems = extensions.findall('.//*[@seconds]')
                    if seconds_elems:
                        for sec_elem in seconds_elems:
                            print(f'    Punkt {j+1}: {lat}, {lon}, alt={alt}, seconds={sec_elem.get("seconds")}')
                            time_found = True
                            break
            
            if not time_found:
                print(f'    Punkt {j+1}: {lat}, {lon}, alt={alt}, BRAK CZASU')
        
        # Sprawdź ostatnie 5 punktów
        if len(track_points) > 5:
            print('  Ostatnie 5 punktów:')
            for j, point in enumerate(track_points[-5:], len(track_points)-4):
                lat = point.get('lat')
                lon = point.get('lon')
                extensions = point.find('.//{http://www.topografix.com/GPX/1/1}extensions')
                if extensions is not None:
                    clock_elem = extensions.find('.//*[@clock]')
                    if clock_elem is not None:
                        print(f'    Punkt {j}: clock={clock_elem.get("clock")}')
                    else:
                        print(f'    Punkt {j}: BRAK CZASU')
                else:
                    print(f'    Punkt {j}: BRAK ROZSZERZEŃ')
        
except Exception as e:
    print(f'Błąd: {e}')
