import pandas as pd

df = pd.read_csv('data/output/gps_master.csv')

# Pokaż tylko trasy z kaloriami
with_calories = df[df['route_total_calories'].notna()]
print('Trasy z kaloriami:')
print(with_calories[['track_name', 'route_total_calories', 'route_distance_km']].drop_duplicates().head(10).to_string())

print('\n\nStatystyki kalorii:')
print(f'Liczba tras z kaloriami: {with_calories["track_name"].nunique()}')
print(f'Zakres kalorii: {with_calories["route_total_calories"].min()} - {with_calories["route_total_calories"].max()}')

print('\n\nTrasy bez kalorii:')
without_calories = df[df['route_total_calories'].isna()]
print(f'Liczba tras bez kalorii: {without_calories["track_name"].nunique()}')
print(without_calories[['track_name', 'source_file']].drop_duplicates().head(10).to_string())
