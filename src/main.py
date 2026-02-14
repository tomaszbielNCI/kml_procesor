import argparse
import os
import sys
from pathlib import Path

# Dodanie ścieżki do core
sys.path.append(os.path.join(os.path.dirname(__file__), 'core'))

from converter import convert_gpx_to_kml, convert_kml_to_gpx
from analyzer import RouteAnalyzer


def main():
    parser = argparse.ArgumentParser(description='KML/GPX Processor - New Architecture')
    parser.add_argument('--action',
                        choices=['convert', 'analyze', 'master-csv', 'batch'],
                        default='convert',
                        help='Actions: convert (single), batch (bulk), analyze, master-csv')
    parser.add_argument('--input',
                        default='data/input',
                        help='Path to input file/folder')
    parser.add_argument('--output',
                        default='data/output',
                        help='Path to output file/folder')
    parser.add_argument('--from-format',
                        choices=['gpx', 'kml'],
                        help='Source format (for conversion)')
    parser.add_argument('--to-format',
                        choices=['gpx', 'kml'],
                        help='Target format (for conversion)')
    parser.add_argument('--file',
                        help='Specific file to convert (optional)')

    args = parser.parse_args()

    # Ensure output folder exists
    os.makedirs(args.output, exist_ok=True)

    if args.action == 'convert':
        if not args.file or not args.from_format or not args.to_format:
            print("For single conversion provide: --file, --from-format, --to-format")
            return
        
        input_path = os.path.join(args.input, args.file)
        output_file = Path(args.file).stem + f".{args.to_format}"
        output_path = os.path.join(args.output, output_file)
        
        print(f"Conversion: {args.file} ({args.from_format}) → {output_file} ({args.to_format})")
        
        if args.from_format == 'gpx' and args.to_format == 'kml':
            convert_gpx_to_kml(input_path, output_path)
        elif args.from_format == 'kml' and args.to_format == 'gpx':
            convert_kml_to_gpx(input_path, output_path)
        else:
            print("Unsupported conversion!")
            return
            
        print(f"✓ Completed: {output_path}")

    elif args.action == 'batch':
        if not args.from_format or not args.to_format:
            print("For batch conversion provide: --from-format, --to-format")
            return
        
        # Import batch function
        sys.path.append(os.path.join(os.path.dirname(__file__), 'scripts'))
        from batch_convert import batch_convert
        
        converted = batch_convert(args.input, args.output, args.from_format, args.to_format)
        print(f"Converted {len(converted)} files")

    elif args.action == 'master-csv':
        # Run master CSV script
        sys.path.append(os.path.join(os.path.dirname(__file__), 'scripts'))
        from gpx_to_master_csv import process_all_files
        
        master_csv = os.path.join(args.output, 'gps_master.csv')
        df = process_all_files(args.input, master_csv)
        
        if df is not None:
            print(f"Created master CSV with {len(df)} points")

    elif args.action == 'analyze':
        # Data analysis
        master_csv = os.path.join(args.output, 'gps_master.csv')
        if not os.path.exists(master_csv):
            print("First run --action master-csv")
            return
            
        analyzer = RouteAnalyzer(master_csv)
        stats = analyzer.get_basic_stats()
        print("=== Analysis Statistics ===")
        for key, value in stats.items():
            print(f"{key}: {value}")


if __name__ == "__main__":
    main()
