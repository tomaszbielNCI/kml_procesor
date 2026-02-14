import pandas as pd
import xml.etree.ElementTree as ET

# Read backup file
backup_file = 'data/input/full_backup_1_Jun_2025_10_24_46.gpx'

print('=== TIME SEQUENCE ANALYSIS IN BACKUP FILE ===')

try:
    # Parse GPX
    tree = ET.parse(backup_file)
    root = tree.getroot()
    
    # Find first track with points
    tracks = root.findall('.//{http://www.topografix.com/GPX/1/1}trk')
    
    for i, track in enumerate(tracks):
        name_elem = track.find('.//{http://www.topografix.com/GPX/1/1}name')
        track_name = name_elem.text if name_elem is not None else 'No name'
        
        # Find all points in track
        track_points = track.findall('.//{http://www.topografix.com/GPX/1/1}trkpt')
        
        if len(track_points) > 0:
            print(f'\n=== TRACK {i+1}: {track_name} ===')
            print(f'Total points: {len(track_points)}')
            
            # Collect time data from first 20 points
            time_data = []
            for j, point in enumerate(track_points[:20]):
                extensions = point.find('.//{http://www.topografix.com/GPX/1/1}extensions')
                if extensions is not None:
                    clock_elem = extensions.find('.//*[@clock]')
                    seconds_elem = extensions.find('.//*[@seconds]')
                    
                    clock_time = clock_elem.get('clock') if clock_elem is not None else 'N/A'
                    seconds = seconds_elem.get('seconds') if seconds_elem is not None else 'N/A'
                    
                    time_data.append((j+1, clock_time, seconds))
                    print(f'Point {j+1:2d}: clock={clock_time}, seconds={seconds}')
            
            # Check if time increments by approximately 60 seconds
            print('\n=== TIME INCREMENT ANALYSIS ===')
            if len(time_data) > 1:
                for j in range(1, len(time_data)):
                    prev_seconds = int(time_data[j-1][2]) if time_data[j-1][2] != 'N/A' else 0
                    curr_seconds = int(time_data[j][2]) if time_data[j][2] != 'N/A' else 0
                    
                    if prev_seconds > 0 and curr_seconds > 0:
                        diff = curr_seconds - prev_seconds
                        print(f'Point {time_data[j][0]} - Point {time_data[j-1][0]}: {diff} seconds difference')
            
            # Check last few points
            print('\n=== LAST 5 POINTS ===')
            for j, point in enumerate(track_points[-5:], len(track_points)-4):
                extensions = point.find('.//{http://www.topografix.com/GPX/1/1}extensions')
                if extensions is not None:
                    clock_elem = extensions.find('.//*[@clock]')
                    seconds_elem = extensions.find('.//*[@seconds]')
                    
                    clock_time = clock_elem.get('clock') if clock_elem is not None else 'N/A'
                    seconds = seconds_elem.get('seconds') if seconds_elem is not None else 'N/A'
                    
                    print(f'Point {j}: clock={clock_time}, seconds={seconds}')
            
            break  # Only first track with points
            
except Exception as e:
    print(f'Error: {e}')
    import traceback
    traceback.print_exc()
