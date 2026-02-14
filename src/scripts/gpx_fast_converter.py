#!/usr/bin/env python3
"""
gpx_fast_converter.py
OPTIMIZED converter for GPX files only → master CSV
Fast processing, full data, no duplicates
"""

import os
import sys
import pandas as pd
import gpxpy
from pathlib import Path
import hashlib
from datetime import datetime
import re
import xml.etree.ElementTree as ET

def extract_route_stats(description):
    """Fast extraction of stats from description"""
    if not description:
        return {}
    
    stats = {}
    
    # Regex patterns
    patterns = {
        'route_date': r'Date:\s*(\d{2}/\d{2}/\d{4})',
        'route_distance_km': r'Distance:\s*([\d.]+)\s*km',
        'route_time': r'Time:\s*([\d:]+)',
        'route_min_altitude': r'Minimum Altitude:\s*([-]?\d+\.?\d*)\s*meters',
        'route_max_altitude': r'Maximum Altitude:\s*([-]?\d+\.?\d*)\s*meters',
        'route_total_calories': r'Energy Consumption:\s*(\d+)\s*Calories'
    }
    
    for key, pattern in patterns.items():
        match = re.search(pattern, description)
        if match:
            if key == 'route_distance_km' or 'altitude' in key:
                stats[key] = float(match.group(1))
            elif 'calories' in key:
                stats[key] = int(match.group(1))
            else:
                stats[key] = match.group(1)
    
    return stats

def extract_time_from_extensions(point):
    """Extract time data from GPX extensions"""
    try:
        # Get extensions element
        extensions = point.extensions
        if not extensions:
            return None, None
        
        # Find TrackPointExtension
        for elem in extensions.extensions:
            if hasattr(elem, 'tag') and 'TrackPointExtension' in elem.tag:
                # Look for clock and seconds
                clock_time = None
                seconds = None
                
                for child in elem.children:
                    if hasattr(child, 'tag'):
                        tag_name = child.tag.split('}')[-1] if '}' in child.tag else child.tag
                        if tag_name == 'clock' and hasattr(child, 'text'):
                            clock_time = child.text
                        elif tag_name == 'seconds' and hasattr(child, 'text'):
                            seconds = child.text
                
                return clock_time, seconds
        
        return None, None
    except:
        return None, None

def extract_time_from_xml(point_xml):
    """Extract time from raw XML element"""
    try:
        extensions = point_xml.find('.//{http://www.topografix.com/GPX/1/1}extensions')
        if extensions is not None:
            track_ext = extensions.find('.//{http://www.garmin.com/xmlschemas/TrackPointExtension/v1}TrackPointExtension')
            if track_ext is not None:
                clock_elem = track_ext.find('.//{http://www.garmin.com/xmlschemas/TrackPointExtension/v1}clock')
                seconds_elem = track_ext.find('.//{http://www.garmin.com/xmlschemas/TrackPointExtension/v1}seconds')
                
                clock_time = clock_elem.text if clock_elem is not None else None
                seconds = seconds_elem.text if seconds_elem is not None else None
                
                return clock_time, seconds
        
        return None, None
    except:
        return None, None

def process_gpx_fast(gpx_file_path):
    """Lightning fast GPX processing with enhanced time extraction"""
    filename = os.path.basename(gpx_file_path)
    print(f'GPX: {filename}')
    
    try:
        # Check if it's a backup file with time extensions
        is_backup_file = 'full_backup' in filename
        
        # Fast loading
        with open(gpx_file_path, 'r', encoding='utf-8') as f:
            gpx = gpxpy.parse(f)
        
        track_data = []
        file_hash = hashlib.md5(open(gpx_file_path, 'rb').read()).hexdigest()
        
        # For backup files, also parse with ElementTree to get extensions
        backup_tree = None
        if is_backup_file:
            try:
                backup_tree = ET.parse(gpx_file_path)
            except:
                pass
        
        for track_idx, track in enumerate(gpx.tracks):
            # Stats from description
            route_stats = extract_route_stats(track.description)
            
            # Route timestamp (first point OR from name)
            route_timestamp = None
            route_date = None
            
            if track.segments and track.segments[0].points:
                first_point = track.segments[0].points[0]
                route_timestamp = first_point.time.isoformat() if first_point.time else None
                
                # Extract date from first point time if no route_date from description
                if route_timestamp and 'route_date' not in route_stats:
                    try:
                        dt = datetime.fromisoformat(route_timestamp.replace('Z', '+00:00'))
                        route_date = dt.strftime('%d/%m/%Y')
                    except:
                        pass
            
            # If no time in points, try to extract from name
            if route_timestamp is None and track.name:
                # Search for date in track name
                date_match = re.search(r'(\d{2}/\d{2}/\d{4})', track.name)
                if date_match:
                    date_str = date_match.group(1)
                    # Add sample time
                    route_timestamp = f"{date_str}T09:00:00+00:00"
                    route_date = date_str
            
            # Add route_date if extracted from time
            if route_date and 'route_date' not in route_stats:
                route_stats['route_date'] = route_date
            
            # Get backup track points for time extraction
            backup_track_points = None
            if backup_tree and is_backup_file:
                backup_tracks = backup_tree.findall('.//{http://www.topografix.com/GPX/1/1}trk')
                if track_idx < len(backup_tracks):
                    backup_track_points = backup_tracks[track_idx].findall('.//{http://www.topografix.com/GPX/1/1}trkpt')
            
            for seg_idx, segment in enumerate(track.segments):
                for point_idx, point in enumerate(segment.points):
                    # Try to extract time from extensions first
                    point_time = None
                    clock_time = None
                    seconds = None
                    
                    if point.time:
                        point_time = point.time.isoformat()
                    elif backup_track_points and point_idx < len(backup_track_points):
                        # Extract from backup XML
                        clock_time, seconds = extract_time_from_xml(backup_track_points[point_idx])
                        if clock_time:
                            point_time = clock_time
                    
                    # If still no time, try gpxpy extensions
                    if not point_time:
                        clock_time, seconds = extract_time_from_extensions(point)
                        if clock_time:
                            point_time = clock_time
                    
                    if not point_time:
                        point_time = 'no_time'
                    
                    # Unique ID
                    point_id = f"{point.latitude:.6f}_{point.longitude:.6f}_{point_time}"
                    
                    track_data.append({
                        'unique_point_id': point_id,
                        'track_name': track.name or f"Track_{len(track_data)}",
                        'latitude': point.latitude,
                        'longitude': point.longitude,
                        'altitude': point.elevation or 0.0,
                        'time': point_time,
                        'route_timestamp': route_timestamp,
                        'source_file': filename,
                        'file_hash': file_hash,
                        'file_type': 'gpx',
                        'track_description': track.description,
                        'processed_timestamp': datetime.now().isoformat(),
                        'point_clock': clock_time,  # NEW - clock time from extensions
                        'point_seconds': seconds,   # NEW - seconds from extensions
                        **route_stats  # Add route stats
                    })
        
        return track_data
        
    except Exception as e:
        print(f'Error: {filename} - {e}')
        return []

def create_gpx_master_csv(input_dir, output_csv):
    """Fast creation of master CSV from GPX only"""
    
    print('GPX FAST CONVERTER -> MASTER CSV')
    print('=' * 50)
    
    input_path = Path(input_dir)
    gpx_files = list(input_path.glob("*.gpx"))
    
    print(f'Found {len(gpx_files)} GPX files')
    
    all_data = []
    processed_files = []
    
    for gpx_file in gpx_files:
        track_data = process_gpx_fast(str(gpx_file))
        
        if track_data:
            all_data.extend(track_data)
            processed_files.append(gpx_file.name)
            print(f'  {len(track_data)} points')
    
    if not all_data:
        print('No data!')
        return None
    
    # DataFrame and duplicate removal
    master_df = pd.DataFrame(all_data)
    initial_count = len(master_df)
    master_df = master_df.drop_duplicates(subset=['unique_point_id'], keep='first')
    removed = initial_count - len(master_df)
    
    # Sorting
    master_df = master_df.sort_values(['source_file', 'track_name']).reset_index(drop=True)
    
    # Save to CSV
    master_df.to_csv(output_csv, index=False, encoding='utf-8')
    
    # Statistics
    print("\n" + "=" * 50)
    print('STATISTICS')
    print("=" * 50)
    print(f'Files: {len(processed_files)}')
    print(f'Points: {len(master_df)} (removed {removed} duplicates)')
    print(f'Tracks: {master_df["track_name"].nunique()}')
    print(f'Altitude: {master_df["altitude"].min():.1f} - {master_df["altitude"].max():.1f} m')
    
    if 'route_total_calories' in master_df.columns:
        calories = master_df['route_total_calories'].dropna()
        if not calories.empty:
            print(f'Calories: {calories.min()} - {calories.max()} kcal (avg {calories.mean():.0f})')
    
    # Time statistics
    has_time = master_df['time'] != 'no_time'
    print(f'Points with time: {has_time.sum()} / {len(master_df)}')
    
    if 'point_clock' in master_df.columns:
        has_clock = master_df['point_clock'].notna()
        print(f'Points with clock: {has_clock.sum()} / {len(master_df)}')
    
    print(f'Saved to: {output_csv}')
    print(f'Size: {os.path.getsize(output_csv) / 1024 / 1024:.1f} MB')
    
    return master_df

def main():
    """Main function"""
    base_dir = os.path.dirname(__file__)
    # Go up to project root, then to data folder
    project_root = os.path.dirname(os.path.dirname(base_dir))
    input_dir = os.path.join(project_root, 'data', 'input')
    output_dir = os.path.join(project_root, 'data', 'output')
    
    os.makedirs(output_dir, exist_ok=True)
    output_csv = os.path.join(output_dir, 'gps_master.csv')
    
    master_df = create_gpx_master_csv(input_dir, output_csv)
    
    if master_df is not None:
        print(f'\nColumns: {list(master_df.columns)}')
        print(f'\nFirst 3 rows:')
        print(master_df.head(3).to_string())
        return master_df
    
    return None

if __name__ == "__main__":
    main()
