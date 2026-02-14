import pandas as pd
import re

df = pd.read_csv('data/output/gps_master.csv')

# Tylko backup pliki
backup_files = df[df['source_file'].str.contains('full_backup', na=False)]

print('=== BACKUP TIME EXTENSION ANALYSIS ===')
print(f'Backup points: {len(backup_files)}')

# Sprawdź czy w danych są rozszerzenia GPX z czasem
print('\n=== Checking for time in track point extensions ===')

# Przyjrzyj się próbce danych z backup
sample_backup = backup_files.head(100)
print(f'Sample backup points: {len(sample_backup)}')

# Sprawdź unikalne wartości w kolumnach związanych z czasem
time_columns = ['time', 'route_timestamp', 'route_date']
for col in time_columns:
    if col in backup_files.columns:
        unique_vals = backup_files[col].value_counts()
        print(f'\n{col}: {len(unique_vals)} unique values')
        print(f'Top 5 values: {list(unique_vals.head(5).index)}')

# Sprawdź czy w nazwach tras są daty i czasy
print('\n=== Track name time patterns ===')
track_names = backup_files['track_name'].unique()
print(f'Unique tracks: {len(track_names)}')

# Wzorce czasowe w nazwach
time_patterns = []
for name in track_names[:20]:
    # Szukaj wzorców czasu HH:MM
    time_match = re.search(r'\d{1,2}:\d{2}', name)
    if time_match:
        time_patterns.append((name, time_match.group()))
        print(f'Track with time: {name} -> {time_match.group()}')

print(f'\nFound {len(time_patterns)} tracks with time patterns in names')

# Sprawdź czy route_timestamp pochodzi z daty w nazwie trasy
print('\n=== Route timestamp vs track name date ===')
for track_name in backup_files['track_name'].unique()[:10]:
    track_data = backup_files[backup_files['track_name'] == track_name]
    route_ts = track_data['route_timestamp'].iloc[0] if pd.notna(track_data['route_timestamp'].iloc[0]) else 'NO_TS'
    
    # Wyciągnij datę z nazwy
    date_match = re.search(r'(\d{2}/\d{2}/\d{4})', track_name)
    if date_match:
        track_date = date_match.group(1)
        print(f'{track_name[:50]}... | Route TS: {route_ts} | Track date: {track_date}')
    else:
        print(f'{track_name[:50]}... | Route TS: {route_ts} | No date in name')
