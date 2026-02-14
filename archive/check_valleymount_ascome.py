import pandas as pd

# Load data
df = pd.read_csv('data/output/gps_master.csv')

# Find Valleymount to Blessington route
valleymount_route = df[df['track_name'] == 'valleymount to blessington  12/10/2025 09:22']

print(f'Route: valleymount to blessington  12/10/2025 09:22')
print(f'Points: {len(valleymount_route)}')
print(f'Latitude range: {valleymount_route["latitude"].min():.6f} - {valleymount_route["latitude"].max():.6f}')
print(f'Longitude range: {valleymount_route["longitude"].min():.6f} - {valleymount_route["longitude"].max():.6f}')
print(f'Altitude range: {valleymount_route["altitude"].min():.1f} - {valleymount_route["altitude"].max():.1f} m')

# Check for Ascome/Ascombe
print('\n=== Searching for Ascome/Ascombe ===')
ascome_routes = df[df['track_name'].str.contains('ascome|ascombe', case=False, na=False)]
print(f'Routes with ascome/ascombe: {len(ascome_routes)}')
for name in ascome_routes['track_name'].unique():
    print(f'  {name}')

# Check if we need to add Ascombe
if len(ascome_routes) == 0:
    print('\nNo Ascome/Ascombe route found. You mentioned getting in car at Ascombe.')
    print('Would you like me to add this as a separate route or modify the existing Valleymount route?')
