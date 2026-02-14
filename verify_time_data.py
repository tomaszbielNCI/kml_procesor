import pandas as pd

df = pd.read_csv('data/output/gps_master.csv')

print('=== TIME DATA VERIFICATION ===')
print(f'Total points: {len(df)}')

# Check time columns
time_columns = ['time', 'point_clock', 'point_seconds']
for col in time_columns:
    if col in df.columns:
        non_null = df[col].notna().sum()
        print(f'{col}: {non_null} / {len(df)} points have data')

# Check backup files specifically
backup_files = df[df['source_file'].str.contains('full_backup', na=False)]
print(f'\nBackup files: {len(backup_files)} points')

for col in time_columns:
    if col in df.columns:
        non_null = backup_files[col].notna().sum()
        print(f'Backup {col}: {non_null} / {len(backup_files)} points have data')

# Sample backup data
print('\n=== Sample backup points with time ===')
backup_sample = backup_files[backup_files['point_clock'].notna()].head(5)
for idx, row in backup_sample.iterrows():
    print(f"Track: {row['track_name'][:30]}...")
    print(f"  Time: {row['time']}")
    print(f"  Clock: {row['point_clock']}")
    print(f"  Seconds: {row['point_seconds']}")
    print(f"  Alt: {row['altitude']:.1f}m")
    print()
