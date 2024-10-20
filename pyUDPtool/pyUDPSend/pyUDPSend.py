import pandas as pd
import json
import socket
import struct
import argparse

# Function to map and pack a value based on its type
def pack_value(value, dtype):
    """Convert value to bytes based on its type."""
    if pd.isna(value):  # Handle NaN or missing values
        return b''  # Empty bytes for missing values
    
    # Type conversion and packing to bytes for different types
    if dtype == "float":
        return struct.pack('f', float(value))  # 4 bytes for float
    elif dtype == "double":
        return struct.pack('d', float(value))  # 8 bytes for double
    elif dtype == "int":
        return struct.pack('i', int(value))    # 4 bytes for int
    elif dtype == "bool":
        return struct.pack('?', bool(int(value)))  # 1 byte for bool
    elif dtype == "str":
        encoded_str = value.encode('utf-8')
        return struct.pack(f'{len(encoded_str)}s', encoded_str)  # Variable-length string
    elif dtype == "byte":
        return struct.pack('B', int(value))  # 1 byte for unsigned byte
    elif dtype == "char":
        return struct.pack('c', value.encode('utf-8'))  # 1 byte for single char
    else:
        raise ValueError(f"Unsupported data type: {dtype}")

# Function to load JSON from a file
def load_json(json_file):
    """Load JSON from a file with UTF-8 encoding."""
    with open(json_file, 'r', encoding='utf-8') as file:  # Specify UTF-8 encoding
        return json.load(file)

# Function to load CSV, cast types, and send rows via UDP
def load_cast_and_send_udp(castType, csv_file, ip, port):
    """Load CSV, cast columns, and send rows via UDP based on the JSON type descriptions."""
    # Load CSV
    df = pd.read_csv(csv_file)

    # Load JSON with column types
    column_types = load_json(castType)
    df.columns = column_types.keys()

    # Create UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Loop through each row in the DataFrame
    for index, row in df.iterrows():
        row_data = b''  # Initialize an empty byte stream for the row
        
        # Pack all columns into a single byte stream
        for column, dtype in column_types.items():
            if column in row.index:
                row_data += pack_value(row[column], dtype)  # Concatenate packed bytes for each column
        
        # Send the entire row as a single UDP packet
        print(row_data)
        sock.sendto(row_data, (ip, port))

    # Close the socket after sending
    sock.close()

# Main function to handle command-line arguments
def main():
    # Argument parser for command-line input
    parser = argparse.ArgumentParser(description='Send CSV data over UDP based on JSON column type description.')
    
    parser.add_argument('castType', type=str, help='Path to the cast type file. must be wrote in json')
    parser.add_argument('csv_file', type=str, help='Path to the CSV file.')
    parser.add_argument('ip', type=str, help='Destination IP address for UDP transmission.')
    parser.add_argument('port', type=int, help='Destination port for UDP transmission.')

    # Parse the arguments
    args = parser.parse_args()

    # Call the function to load, cast, and send data
    load_cast_and_send_udp(args.castType, args.csv_file, args.ip, args.port)

# Run the main function when the script is executed
if __name__ == "__main__":
    main()
