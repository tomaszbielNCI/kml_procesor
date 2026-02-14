import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Load data
df = pd.read_csv('data/output/gps_master.csv')

# Get Valleymount to Blessington route
valleymount_route = df[df['track_name'] == 'valleymount to blessington  12/10/2025 09:22'].copy()

print(f'Route: valleymount to blessington  12/10/2025 09:22')
print(f'Total points: {len(valleymount_route)}')

# Convert time data
valleymount_route['time_seconds'] = pd.to_numeric(valleymount_route['point_seconds'], errors='coerce')
valleymount_route['time_minutes'] = valleymount_route['time_seconds'] / 60

# Remove rows with missing time data
valleymount_route = valleymount_route.dropna(subset=['time_seconds'])

# Calculate distance and speed properly
valleymount_route = valleymount_route.reset_index(drop=True)
valleymount_route['lat_diff'] = valleymount_route['latitude'].diff()
valleymount_route['lon_diff'] = valleymount_route['longitude'].diff()
valleymount_route['time_diff'] = valleymount_route['time_seconds'].diff()

# Calculate distance using Haversine approximation
valleymount_route['distance_km'] = np.sqrt(
    valleymount_route['lat_diff']**2 + valleymount_route['lon_diff']**2
) * 111  # Approximate conversion

# Calculate speed (avoiding division by zero)
valleymount_route['speed_kmh'] = np.where(
    valleymount_route['time_diff'] > 0,
    (valleymount_route['distance_km'] / valleymount_route['time_diff']) * 3600,
    0
)

# Remove unrealistic speeds (> 150 km/h)
valleymount_route['speed_kmh'] = np.where(
    valleymount_route['speed_kmh'] > 150,
    np.nan,
    valleymount_route['speed_kmh']
)

print(f'Points with valid speed: {valleymount_route["speed_kmh"].notna().sum()}')

# Create Anscombe's quartet-like analysis
fig, axes = plt.subplots(2, 2, figsize=(15, 12))
fig.suptitle("Anscombe's Quartet Analysis - Valleymount to Blessington Route", fontsize=16)

# Dataset 1: Time vs Altitude (original relationship)
axes[0, 0].scatter(valleymount_route['time_minutes'], valleymount_route['altitude'], alpha=0.6)
axes[0, 0].set_title('Dataset I: Time vs Altitude')
axes[0, 0].set_xlabel('Time (minutes)')
axes[0, 0].set_ylabel('Altitude (m)')
axes[0, 0].grid(True, alpha=0.3)

# Dataset 2: Time vs Speed (derived from distance between points)
valid_speed_data = valleymount_route.dropna(subset=['speed_kmh'])
axes[0, 1].scatter(valid_speed_data['time_minutes'], 
                   valid_speed_data['speed_kmh'], alpha=0.6, color='orange')
axes[0, 1].set_title('Dataset II: Time vs Speed')
axes[0, 1].set_xlabel('Time (minutes)')
axes[0, 1].set_ylabel('Speed (km/h)')
axes[0, 1].grid(True, alpha=0.3)

# Dataset 3: Latitude vs Longitude (spatial pattern)
axes[1, 0].scatter(valleymount_route['longitude'], 
                   valleymount_route['latitude'], alpha=0.6, color='green')
axes[1, 0].set_title('Dataset III: Longitude vs Latitude')
axes[1, 0].set_xlabel('Longitude')
axes[1, 0].set_ylabel('Latitude')
axes[1, 0].grid(True, alpha=0.3)

# Dataset 4: Time vs Altitude (last 25% - car journey)
last_25_percent = valleymount_route.tail(int(len(valleymount_route) * 0.25))
axes[1, 1].scatter(last_25_percent['time_minutes'], 
                   last_25_percent['altitude'], alpha=0.6, color='red')
axes[1, 1].set_title('Dataset IV: Time vs Altitude (Last 25% - Car Journey)')
axes[1, 1].set_xlabel('Time (minutes)')
axes[1, 1].set_ylabel('Altitude (m)')
axes[1, 1].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('valleymount_anscombe_quartet.png', dpi=300, bbox_inches='tight')
plt.show()

# Summary statistics for each dataset
print('\n=== SUMMARY STATISTICS ===')

# Dataset 1: Time vs Altitude
print('\nDataset I: Time vs Altitude')
print(f'Time: mean={valleymount_route["time_minutes"].mean():.1f}, std={valleymount_route["time_minutes"].std():.1f}')
print(f'Altitude: mean={valleymount_route["altitude"].mean():.1f}, std={valleymount_route["altitude"].std():.1f}')
print(f'Correlation: {valleymount_route["time_minutes"].corr(valleymount_route["altitude"]):.3f}')

# Dataset 2: Time vs Speed
print('\nDataset II: Time vs Speed')
print(f'Time: mean={valid_speed_data["time_minutes"].mean():.1f}, std={valid_speed_data["time_minutes"].std():.1f}')
print(f'Speed: mean={valid_speed_data["speed_kmh"].mean():.1f}, std={valid_speed_data["speed_kmh"].std():.1f}')
print(f'Correlation: {valid_speed_data["time_minutes"].corr(valid_speed_data["speed_kmh"]):.3f}')

# Dataset 3: Longitude vs Latitude
print('\nDataset III: Longitude vs Latitude')
print(f'Longitude: mean={valleymount_route["longitude"].mean():.6f}, std={valleymount_route["longitude"].std():.6f}')
print(f'Latitude: mean={valleymount_route["latitude"].mean():.6f}, std={valleymount_route["latitude"].std():.6f}')
print(f'Correlation: {valleymount_route["longitude"].corr(valleymount_route["latitude"]):.3f}')

# Dataset 4: Last 25% - Car journey
print('\nDataset IV: Time vs Altitude (Last 25% - Car Journey)')
print(f'Time: mean={last_25_percent["time_minutes"].mean():.1f}, std={last_25_percent["time_minutes"].std():.1f}')
print(f'Altitude: mean={last_25_percent["altitude"].mean():.1f}, std={last_25_percent["altitude"].std():.1f}')
print(f'Correlation: {last_25_percent["time_minutes"].corr(last_25_percent["altitude"]):.3f}')

# Additional analysis: Speed changes (walking vs car)
print('\n=== SPEED ANALYSIS (Walking vs Car) ===')
walking_data = valleymount_route.head(int(len(valleymount_route) * 0.75))
car_data = last_25_percent

walking_speed = walking_data['speed_kmh'].dropna()
car_speed = car_data['speed_kmh'].dropna()

print(f'Walking phase: {len(walking_speed)} points')
print(f'  Average speed: {walking_speed.mean():.1f} km/h')
print(f'  Max speed: {walking_speed.max():.1f} km/h')

print(f'Car phase: {len(car_speed)} points')
print(f'  Average speed: {car_speed.mean():.1f} km/h')
print(f'  Max speed: {car_speed.max():.1f} km/h')

# Create speed comparison plot
plt.figure(figsize=(12, 6))
plt.plot(valleymount_route['time_minutes'], 
         valleymount_route['speed_kmh'].fillna(0), 
         alpha=0.7, label='Speed over time')
plt.axvline(x=walking_data['time_minutes'].max(), color='red', 
            linestyle='--', label='Transition to car')
plt.xlabel('Time (minutes)')
plt.ylabel('Speed (km/h)')
plt.title('Speed Changes - Valleymount to Blessington Route')
plt.legend()
plt.grid(True, alpha=0.3)
plt.savefig('valleymount_speed_analysis.png', dpi=300, bbox_inches='tight')
plt.show()

print('\n=== TRANSITION POINT ANALYSIS ===')
transition_idx = len(walking_data)
transition_point = valleymount_route.iloc[transition_idx]
print(f'Transition point (getting in car):')
print(f'  Time: {transition_point["time_minutes"]:.1f} minutes')
print(f'  Location: {transition_point["latitude"]:.6f}, {transition_point["longitude"]:.6f}')
print(f'  Altitude: {transition_point["altitude"]:.1f} m')

print('\nAnalysis complete! Check the generated plots:')
print('- valleymount_anscombe_quartet.png')
print('- valleymount_speed_analysis.png')
