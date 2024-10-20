import pandas as pd
import socket
import struct
import argparse
from pyUDPSend import pack_value, load_json

# Function to load CSV, cast types, and send rows via UDP, include header bytes as described in settings.json
def exc_m2_udp(settings):
    """Load CSV, cast columns, and send rows via UDP based on the JSON type descriptions."""
    
    header  = bytes.fromhex(settings['header'][2:])
    castType  = settings['castType']
    csv_file  = settings['csv_file']
    ip  = settings['ip']
    port = settings['port']
    checksumNote  = settings['checksumNote']
    
    
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
        
        for head_i in header :
            row_data += pack_value(head_i,'byte')
        # Pack all columns into a single byte stream
        for column, dtype in column_types.items():
            if column in row.index:
                row_data += pack_value(row[column], dtype)  # Concatenate packed bytes for each column
        
        # checksum subroutine 
        if checksumNote == True:            
            row_data += pack_value(checksum_(row_data), 'byte')
        
        # Send the entire row as a single UDP packet
        print(row_data)
        sock.sendto(row_data, (ip, port))

    # Close the socket after sending
    sock.close()
    
def checksum_(data):
    CRC = 0 
    for data_k in data:
        CRC = CRC + data_k
    CRC = 0xFF - CRC%256
    return CRC

# Main function to handle command-line arguments
def main():

    str_help= '''
        #pyUDPm2 
            It sends arbirary data stream (csv form) according to designated cast type for each column.
            in mode2, it can have predefined header bytes in front and checksum byte in tail. 
            for the setting, you need to edit a settings.json file. see ex_setting.json 
        #syntax : follow json format 
        #component : castType, csv_file, ip, port, header, checksumFlag
        #ex <ex_setting.json>
            {
                "castType": "castType.json",
                "csv_file": "csv_file.csv",
                "ip": "192.168.0.1",
                "port": 5500,
                "header" : "0x000003F264"
                "checksumNote" : 1 #or 0 
            }
        # to run the code, use following syntax
            python pyUDPm2.py ex_setting.json 
        # note 
            header should be described in hex value. and fill zeros for digits preserves
        '''
    print(str_help)
    parser = argparse.ArgumentParser(description=str_help)    
    parser.add_argument('setfile', type=str, help='setting file in json')
    
    # Parse the arguments
    args = parser.parse_args()

    
    try:
        settings = load_json(args.setfile)
        exc_m2_udp(settings)
        return True
        
    except  Exception as err:
        print(f'error occured {err}')
        return False
    
# Run the main function when the script is executed
if __name__ == "__main__":
    main()
