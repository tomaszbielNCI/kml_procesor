import pandas as pd

df = pd.read_csv('data/output/gps_master.csv')

# Tylko backup pliki
backup_files = df[df['source_file'].str.contains('full_backup', na=False)]

print('=== BACKUP PLIKI ANALIZA ===')
print(f'Liczba punktów backup: {len(backup_files)}')
print(f'Liczba unikalnych tras backup: {backup_files["track_name"].nunique()}')

print('\n=== Puste wartości w backup ===')
backup_nulls = backup_files.isnull().sum()
print(backup_nulls[backup_nulls > 0])

print('\n=== Przykładowe trasy backup ===')
for track_name in backup_files['track_name'].unique()[:5]:
    track_data = backup_files[backup_files['track_name'] == track_name]
    print(f'\nTrasa: {track_name}')
    print(f'  Punktów: {len(track_data)}')
    print(f'  route_timestamp: {track_data["route_timestamp"].iloc[0]}')
    print(f'  route_date: {track_data["route_date"].iloc[0]}')
    print(f'  route_total_calories: {track_data["route_total_calories"].iloc[0]}')
    print(f'  route_distance_km: {track_data["route_distance_km"].iloc[0]}')
    print(f'  time (pierwszy punkt): {track_data["time"].iloc[0]}')

print('\n=== Czas w punktach backup ===')
time_values = backup_files['time'].value_counts()
print(f'Punkty z czasem: {(backup_files["time"] != "no_time").sum()}')
print(f'Punkty bez czasu: {(backup_files["time"] == "no_time").sum()}')

if 'no_time' in time_values.index:
    print(f'Wartość "no_time": {time_values["no_time"]}')
else:
    print('Brak "no_time" - wszystkie punkty mają czas!')
