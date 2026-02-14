import pandas as pd

df = pd.read_csv('data/output/gps_master.csv')
print('Column names in CSV:')
for i, col in enumerate(df.columns):
    print(f'{i+1:2d}. {col}')
    
print('\nChecking route_total_calories column:')
print(f'Data type: {df["route_total_calories"].dtype}')
print(f'Null values: {df["route_total_calories"].isnull().sum()}')
print(f'Sample values: {df["route_total_calories"].head(10).tolist()}')

print('\nChecking route_distance_km column:')
print(f'Data type: {df["route_distance_km"].dtype}')
print(f'Null values: {df["route_distance_km"].isnull().sum()}')
print(f'Sample values: {df["route_distance_km"].head(10).tolist()}')
