#!/usr/bin/python3

import os
import argparse
import json
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
import zstandard as zstd


class FileConverter:
    '''
    Definition: 
    Takes in an input file (CSV, Parquet, JSON) and converts it to ZST.
    If no output 'filepath/output_file.zst' is specified, the input filepath and filename are used, with .zst extension.
    

    Examples: 
    (1) Manually specify only input filepath and filename.
    
    input_file = 'path/to/input_filename.csv'
    python3 file_converter.py input_file
    (Output file written to 'path/to/input_filename.zst')

    (2) Manually specify both input and output filepath and filename.
    
    input_file = 'path/to/input_filename.csv'
    output_file_format = 'json'
    python3 file_converter.py input_file output_file_format
    (Output file written to 'path/to/input_filename.json')

    '''

    def __init__(self):
        pass

    def _detect_format(self, input_file):
        _, file_extension = os.path.splitext(input_file)
        if file_extension == ".csv":
            return "csv"
        elif file_extension == ".parquet":
            return "parquet"
        elif file_extension == ".json":
            return "json"
        else:
            raise ValueError("Unsupported file format. Supported formats: csv, parquet, json")

    def _csv_to_format(self, input_file, output_file, output_file_format):
        # Read CSV data
        df = pd.read_csv(input_file)
        # Convert DataFrame to CSV string
        csv_data = df.to_csv(index=False) ## ??

        if output_file_format == 'zst':
            # Compress the CSV data using Zstandard
            cctx = zstd.ZstdCompressor()
            with open(output_file, 'wb') as f:
                with cctx.stream_writer(f) as compressor:
                    compressor.write(csv_data.encode('utf-8'))
        
        elif output_file_format == 'json': 
            json_data = df.to_json(orient='records')
            with open(output_file, 'w') as json_file:
                json_file.write(json_data)

        elif output_file_format == 'parquet': 
            df.to_parquet(output_file, index=False)

        elif output_file_format == 'csv': 
            print('Input file is already formatted as CSV.')
        else:
            raise ValueError(f"Conversion to {output_file_format} is not supported.")

    def _parquet_to_format(self, input_file, output_file, output_file_format):
        # Read Parquet data
        table = pq.read_table(input_file)
        df = table.to_pandas()
        # Convert DataFrame to CSV string
        csv_data = df.to_csv(index=False)

        if output_file_format == 'zst':
            # Compress the CSV data using Zstandard
            cctx = zstd.ZstdCompressor()
            with open(output_file, 'wb') as f:
                with cctx.stream_writer(f) as compressor:
                    compressor.write(csv_data.encode('utf-8'))
        
        elif output_file_format == 'csv': 
            df.to_csv(output_file, index=False)

        elif output_file_format == 'json': 
            json_data = df.to_json(orient='records')
            with open(output_file, 'w') as json_file:
                json_file.write(json_data)

        elif output_file_format == 'parquet': 
            print('Input file is already formatted as Parquet.')
        else:
            raise ValueError(f"Conversion to {output_file_format} is not supported.")

    def _json_to_format(self, input_file, output_file, output_file_format):
        # Read JSON data
        with open(input_file, 'r') as f:
            json_data = json.load(f)
        # Convert Python dictionary to pandas DataFrame    
        df = pd.DataFrame(json_data)
        # Convert JSON data to string
        json_string = json.dumps(json_data)

        if output_file_format == 'zst':
            # Compress the JSON data using Zstandard
            cctx = zstd.ZstdCompressor()
            with open(output_file, 'wb') as f:
                with cctx.stream_writer(f) as compressor:
                    compressor.write(json_string.encode('utf-8'))
        
        elif output_file_format == 'parquet': 
            # Convert the DataFrame to Arrow table
            table = pa.Table.from_pandas(df)
            # Write Arrow table to Parquet file
            pq.write_table(table, output_file)

        elif output_file_format == 'csv': 
            df.to_csv(output_file, index=False)

        elif output_file_format == 'json': 
            print('Input file is already formatted as JSON object.')
        else:
            raise ValueError(f"Conversion to {output_file_format} is not supported.")

    def convert_to_format(self, input_file, output_file_format=None):
        input_file_format = self._detect_format(input_file)

        # If output file not specified, use input file name with Zstandard extension
        if output_file_format is None:
            output_file = os.path.splitext(input_file)[0] + ".zst"
        else:
            output_file = os.path.splitext(input_file)[0] + f".{output_file_format}"

        if input_file_format == "csv":
            self._csv_to_format(input_file, output_file, output_file_format)
        elif input_file_format == "parquet":
            self._parquet_to_format(input_file, output_file, output_file_format)
        elif input_file_format == "json":
            self._json_to_format(input_file, output_file, output_file_format)


def main():
    parser = argparse.ArgumentParser(description="Convert CSV, Parquet, or JSON files to Zstandard format.")
    parser.add_argument("input_file", type=str, help="Path to the input file.")
    parser.add_argument("output_file_format", type=str, nargs="?", choices=["zst", "json", "csv", "parquet"], help="Output file format (optional; default is None: zst).")

    args = parser.parse_args()

    file_converter = FileConverter()
    file_converter.convert_to_format(args.input_file, args.output_file_format)


if __name__ == "__main__":
    main()
