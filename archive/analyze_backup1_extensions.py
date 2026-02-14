import pandas as pd
import xml.etree.ElementTree as ET

# Read backup file
backup_file = 'data/input/full_backup_1_Jun_2025_10_24_46.gpx'

print('=== DETAILED GPX EXTENSIONS ANALYSIS ===')

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
            print(f'Points count: {len(track_points)}')
            
            # Check first 3 points exactly
            for j, point in enumerate(track_points[:3]):
                print(f'\nPoint {j+1}:')
                
                # Basic data
                lat = point.get('lat')
                lon = point.get('lon')
                print(f'  Coordinates: {lat}, {lon}')
                
                # Elevation
                ele_elem = point.find('.//{http://www.topografix.com/GPX/1/1}ele')
                if ele_elem is not None:
                    print(f'  Elevation: {ele_elem.text}')
                
                # Extensions - full analysis
                extensions = point.find('.//{http://www.topografix.com/GPX/1/1}extensions')
                if extensions is not None:
                    print('  Extensions found:')
                    
                    # Go through all elements in extensions
                    for elem in extensions.iter():
                        if elem.tag:
                            tag_name = elem.tag.split('}')[-1] if '}' in elem.tag else elem.tag
                            print(f'    Tag: {tag_name}')
                            
                            # Print all attributes
                            for attr_name, attr_value in elem.attrib.items():
                                print(f'      {attr_name}: {attr_value}')
                            
                            # Print text if exists
                            if elem.text and elem.text.strip():
                                print(f'      Text: {elem.text.strip()}')
                else:
                    print('  No extensions')
            
            # Check some points from end and middle
            check_indices = []
            if len(track_points) > 10:
                check_indices.append(len(track_points) // 2)  # Middle
                check_indices.append(len(track_points) - 2)    # Second to last
            
            for idx in check_indices:
                if idx < len(track_points):
                    point = track_points[idx]
                    print(f'\nPoint {idx+1} (middle/end):')
                    
                    extensions = point.find('.//{http://www.topografix.com/GPX/1/1}extensions')
                    if extensions is not None:
                        for elem in extensions.iter():
                            if elem.tag:
                                tag_name = elem.tag.split('}')[-1] if '}' in elem.tag else elem.tag
                                if 'clock' in tag_name.lower() or 'seconds' in tag_name.lower() or 'time' in tag_name.lower():
                                    print(f'  TIME: {tag_name}')
                                    for attr_name, attr_value in elem.attrib.items():
                                        print(f'    {attr_name}: {attr_value}')
                    else:
                        print('  No extensions in this point')
            
            break  # Only first track with points
            
except Exception as e:
    print(f'Error: {e}')
    import traceback
    traceback.print_exc()
