import pandas as pd

df = pd.read_csv('data/output/gps_master.csv')

# Tylko backup pliki
backup_files = df[df['source_file'].str.contains('full_backup', na=False)]

print('=== ROUTE TIMESTAMP UNIQUENESS ===')
print(f'Total backup points: {len(backup_files)}')

# Unikalne route_timestamp
unique_timestamps = backup_files['route_timestamp'].dropna().unique()
print(f'Unique route_timestamp values: {len(unique_timestamps)}')

print('\n=== All unique route_timestamp values ===')
for ts in sorted(unique_timestamps):
    count = backup_files[backup_files['route_timestamp'] == ts]['track_name'].nunique()
    print(f'{ts} -> {count} tracks')

print('\n=== Tracks without route_timestamp ===')
no_timestamp = backup_files[backup_files['route_timestamp'].isna()]
print(f'Points without timestamp: {len(no_timestamp)}')
print(f'Unique tracks without timestamp: {no_timestamp["track_name"].nunique()}')

print('\nSample tracks without timestamp:')
for track_name in no_timestamp['track_name'].unique()[:5]:
    track_data = no_timestamp[no_timestamp['track_name'] == track_name]
    print(f'  {track_name}: {len(track_data)} points')

print('\n=== VERIFICATION: Each track should have same timestamp ===')
for track_name in backup_files['track_name'].unique()[:10]:
    track_data = backup_files[backup_files['track_name'] == track_name]
    timestamps = track_data['route_timestamp'].unique()
    if len(timestamps) > 1:
        print(f'ERROR: {track_name} has {len(timestamps)} different timestamps!')
    else:
        ts = timestamps[0] if len(timestamps) == 1 else 'NO_TIMESTAMP'
        print(f'OK: {track_name} -> {ts} ({len(track_data)} points)')
