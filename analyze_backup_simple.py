import pandas as pd

df = pd.read_csv('data/output/gps_master.csv')

# Tylko backup pliki
backup_files = df[df['source_file'].str.contains('full_backup', na=False)]

print('=== BACKUP FILES ANALYSIS ===')
print(f'Backup points: {len(backup_files)}')
print(f'Backup unique tracks: {backup_files["track_name"].nunique()}')

print('\n=== Null values in backup ===')
backup_nulls = backup_files.isnull().sum()
print(backup_nulls[backup_nulls > 0])

print('\n=== Sample backup tracks ===')
for track_name in backup_files['track_name'].unique()[:5]:
    track_data = backup_files[backup_files['track_name'] == track_name]
    print(f'\nTrack: {track_name}')
    print(f'  Points: {len(track_data)}')
    print(f'  route_timestamp: {track_data["route_timestamp"].iloc[0]}')
    print(f'  route_date: {track_data["route_date"].iloc[0]}')
    print(f'  route_total_calories: {track_data["route_total_calories"].iloc[0]}')
    print(f'  route_distance_km: {track_data["route_distance_km"].iloc[0]}')
    print(f'  time (first point): {track_data["time"].iloc[0]}')

print('\n=== Time in backup points ===')
time_values = backup_files['time'].value_counts()
print(f'Points with time: {(backup_files["time"] != "no_time").sum()}')
print(f'Points without time: {(backup_files["time"] == "no_time").sum()}')

if 'no_time' in time_values.index:
    print(f'"no_time" value: {time_values["no_time"]}')
else:
    print('No "no_time" - all points have time!')
