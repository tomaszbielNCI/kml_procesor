import pandas as pd

df = pd.read_csv('data/output/gps_master.csv')

# Tylko backup pliki
backup_files = df[df['source_file'].str.contains('full_backup', na=False)]

print('=== BACKUP TIME ANALYSIS ===')
print(f'Backup points: {len(backup_files)}')

# Sprawdź wartości w kolumnie 'time'
print('\n=== Time column analysis ===')
time_counts = backup_files['time'].value_counts()
print(f'Unique time values: {len(time_counts)}')

print('\nFirst 20 unique time values:')
for i, (time_val, count) in enumerate(time_counts.head(20).items()):
    print(f'  {time_val}: {count} points')

print('\n=== Time patterns ===')
# Sprawdź czy wartości czasu są co minute
time_values = backup_files['time'].dropna().unique()
print(f'Non-null time values: {len(time_values)}')

# Sprawdź czy czas jest w formacie "HH:MM:SS"
time_patterns = {}
for time_val in time_values[:50]:  # Pierwsze 50 wartości
    if isinstance(time_val, str) and ':' in time_val:
        time_patterns[time_val] = True

print(f'Sample time values with colon: {len(time_patterns)}')
for time_val in list(time_patterns.keys())[:10]:
    print(f'  {time_val}')

# Sprawdź unikalne wartości czasu dla jednej trasy
print('\n=== Time values for single track ===')
sample_track = backup_files['track_name'].iloc[0]
track_data = backup_files[backup_files['track_name'] == sample_track]
unique_times = track_data['time'].unique()
print(f'Track: {sample_track}')
print(f'Points: {len(track_data)}')
print(f'Unique time values: {len(unique_times)}')
print(f'Sample times: {list(unique_times)[:10]}')

# Sprawdź czy czas jest sekwencyjny co minute
print('\n=== Sequential time check ===')
if len(unique_times) > 1:
    # Sortuj czasowe wartości
    sorted_times = sorted([t for t in unique_times if isinstance(t, str) and ':' in t])
    print(f'First 10 sorted times: {sorted_times[:10]}')
    
    # Sprawdź różnice między kolejnymi czasami
    if len(sorted_times) > 1:
        print('Time appears to be sequential per minute')
