import os
import pandas as pd
from .converter import gpx_to_df, kml_to_df


class RouteProcessor:
    """Processor for handling GPX/KML route files and merging them into a single DataFrame"""
    
    def __init__(self, input_dir, output_dir):
        self.input_dir = input_dir
        self.output_dir = output_dir
    
    def merge_files(self):
        """Merge all GPX and KML files from input directory into a single DataFrame"""
        all_data = []
        
        if not os.path.exists(self.input_dir):
            raise FileNotFoundError(f"Input directory does not exist: {self.input_dir}")
        
        # Process all files in input directory
        for filename in os.listdir(self.input_dir):
            file_path = os.path.join(self.input_dir, filename)
            
            if filename.lower().endswith('.gpx'):
                try:
                    df = gpx_to_df(file_path)
                    all_data.append(df)
                except Exception as e:
                    print(f"Error processing GPX file {filename}: {e}")
            
            elif filename.lower().endswith('.kml'):
                try:
                    df = kml_to_df(file_path)
                    all_data.append(df)
                except Exception as e:
                    print(f"Error processing KML file {filename}: {e}")
        
        if not all_data:
            raise ValueError("No valid GPX or KML files found in input directory")
        
        # Combine all DataFrames
        merged_df = pd.concat(all_data, ignore_index=True)
        
        # Sort by time if available, otherwise by original order
        if 'time' in merged_df.columns and merged_df['time'].notna().any():
            merged_df['time'] = pd.to_datetime(merged_df['time'])
            merged_df = merged_df.sort_values('time')
        
        return merged_df
