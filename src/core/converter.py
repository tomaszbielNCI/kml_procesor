from simplekml import Kml
from pykml import parser
import gpxpy
import pandas as pd
import os


def df_to_kml(df, output_path):
    """Save DataFrame to KML file"""
    kml = Kml()
    for name, group in df.groupby('placemark'):
        linestring = kml.newlinestring(name=name)
        linestring.coords = [(row['longitude'], row['latitude'], row['altitude'])
                             for _, row in group.iterrows()]
    kml.save(output_path)


def kml_to_df(kml_file):
    """Convert KML to DataFrame"""
    with open(kml_file) as f:
        doc = parser.parse(f).getroot()

    coordinates = []
    for pm in doc.Document.Placemark:
        if hasattr(pm, 'LineString'):
            coords = str(pm.LineString.coordinates).split()
            for coord in coords:
                lon, lat, alt = map(float, coord.split(','))
                coordinates.append({
                    'placemark': str(pm.name),
                    'longitude': lon,
                    'latitude': lat,
                    'altitude': alt,
                    'source_file': os.path.basename(kml_file)
                })
    return pd.DataFrame(coordinates)


def gpx_to_df(gpx_file):
    """Convert GPX to DataFrame with missing altitude handling"""
    with open(gpx_file) as f:
        gpx = gpxpy.parse(f)

    points = []
    for track in gpx.tracks:
        for segment in track.segments:
            for point in segment.points:
                points.append({
                    'placemark': track.name if track.name else os.path.basename(gpx_file),
                    'latitude': point.latitude,
                    'longitude': point.longitude,
                    'altitude': point.elevation if point.elevation is not None else 0.0,
                    'time': point.time.isoformat() if point.time else None,
                    'source_file': os.path.basename(gpx_file)
                })
    return pd.DataFrame(points)


def df_to_gpx(df, output_path, track_name="Converted Track"):
    """Convert DataFrame to GPX file"""
    gpx = gpxpy.gpx.GPX()
    gpx_track = gpxpy.gpx.GPXTrack(name=track_name)
    gpx.tracks.append(gpx_track)
    
    gpx_segment = gpxpy.gpx.GPXTrackSegment()
    gpx_track.segments.append(gpx_segment)
    
    for _, row in df.iterrows():
        point = gpxpy.gpx.GPXTrackPoint(
            latitude=row['latitude'],
            longitude=row['longitude'],
            elevation=row['altitude'] if pd.notna(row['altitude']) else 0.0
        )
        if pd.notna(row.get('time')):
            point.time = pd.to_datetime(row['time'])
        gpx_segment.points.append(point)
    
    with open(output_path, 'w') as f:
        f.write(gpx.to_xml())


def convert_gpx_to_kml(input_path, output_path):
    """Convert GPX → KML"""
    df = gpx_to_df(input_path)
    df_to_kml(df, output_path)
    return output_path


def convert_kml_to_gpx(input_path, output_path, track_name=None):
    """Convert KML → GPX"""
    df = kml_to_df(input_path)
    if not track_name:
        track_name = f"Converted from {os.path.basename(input_path)}"
    df_to_gpx(df, output_path, track_name)
    return output_path
