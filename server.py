import socket
import sys
import time
import os
from analyzemft import mftsession
from datetime import datetime
import zlib

def mapDocxFromMFT(mft_path):
    """
    This function parses the mft and returns
    array of all docx files found in it
    """

    # Array that will save the paths of all docx files 
    docx_array = []
    
    # Start mft processing session
    session = mftsession.MftSession()

    # Set the parser options
    session.mft_options()

    # Set the mft file name (full path)
    session.options.filename = mft_path

    # Open the mft file
    session.open_files()

    # Parse the mft file
    session.process_mft_file()

    # Go over each entry in the mft 
    for entry in session.mft:

        # Get the file name from the entry
        entry_file_name = session.mft[entry]['filename']

        # Check if the file is docx
        if entry_file_name[-5:].lower() == ".docx":

            # Add the file to the docx array  
            docx_array.append(entry_file_name)
            
    # Return the final array 
    return docx_array
            


# Main
def main():

    # Get from command line arguments the path to save the extracted mft 
    saved_mft_path = sys.argv[1]
    
    # Get from command line arguments the log file path 
    log_file_path = sys.argv[2]

    # Get from command line arguments the port 
    port = sys.argv[3]
    
    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to the port
    server_address = ('localhost', int(port))
    print 'starting up on %s port %s' % server_address
    sock.bind(server_address)

    # Listen for incoming connections
    sock.listen(1)

    while True:
        # Wait for a connection
        print 'waiting for a connection'
        connection, client_address = sock.accept()

        try:
            print 'connection from: {}'.format(client_address)
            print 'Waiting for data from the client'
            
            # Receive the data from the client
            while True:
                data = connection.recv(16)

                # Check if data recived
                if data:

                    # Check if the client is going to send file size
                    if data == "size":
                        print "size of the mft file is going to be sent"

                        # Recive the file size from the client
                        size = connection.recv(1024)

                        # Convert the file size from string to int
                        file_size = int(size)
                        print 'file size: {}'.format(file_size)

                        # Set the path for the extracted mft
                        extracted_mft_path = os.path.join(saved_mft_path,"{}_mft_compressed".format(client_address[0]))

                        # Open the empty mft file for writing
                        mft_file = open(extracted_mft_path,'wb')

                        # Count for the bytes that recived from client
                        bytes_recived = 0 

                        
                        # Check if bytes recived is less than the file size
                        while bytes_recived < file_size:

                            # Recive mft content from the client (divided into chunks of 1000000 bytes)
                            mft_contetnt = connection.recv(1000000)

                            # Write the content to the mft file
                            mft_file.write(mft_contetnt)

                            # Add to counter the bytes that recived from client
                            bytes_recived += len(mft_contetnt)


                        # Close the mft file 
                        mft_file.close()
            
                        print "MFT (compressed) extracted succesfuly to: {}".format(extracted_mft_path)

                        # Open the compressed mft file
                        compressed_mft = open(extracted_mft_path,'rb')

                        # Read the compressed mft file
                        compressed_content = compressed_mft.read()

                        # Close the compressed mft file
                        compressed_mft.close()

                        # Open new file to save the decompress mft
                        decompress_mft_path = os.path.join(saved_mft_path,"{}_mft_decompressed".format(client_address[0]))
                        decompress_mft = open(decompress_mft_path,'wb')

                        # Write to the new file the decompress mft
                        decompress_mft.write(zlib.decompress(compressed_content))

                        # Close the decompressed mft file
                        decompress_mft.close()

                        print "MFT decompressed succesfuly and saved to: {}".format(decompress_mft_path)

                        # Get paths of all docx files from the mft
                        docx_paths = mapDocxFromMFT(decompress_mft_path)

                        ##print docx_paths

                        # Get the current timestamp
                        timestamp = str(datetime.now())

                        # Open the log file
                        log_file = open(log_file_path,'a')

                        # Write the details to the log file
                        log_file.write("\n\n{}, {} -".format(client_address[0], timestamp))

                        # Go over each docx in the docx paths array
                        for docx in docx_paths:

                            # Write the docx path to the log file
                            log_file.write("\n{}".format(docx))

                        # Close the log file
                        log_file.close()

                        print "MFT analyzed succesfuly and results saved to log file: {}".format(log_file_path)

                else:
                    print 'no more data from: {}'.format(client_address)
                    break

        finally:
            # Clean up the connection
            connection.close()


main()
