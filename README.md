# Pcysys_Server_python
Waits for data from the malware and every newly arrived MFT, it will map the paths of docx files and will write the details to a log file

USAGE:
-------------------
server.py <folder_path_where_to_save_mft> <path_to_logfile> <listening_port>

EXAMPLE:
-------------------
server.py C:\temp\extractedMFT C:\temp\logfile.txt 20000

REMARKS:
-------------------
- python 2.7 was used
- Reciving all data from client can take a few minutes


OUTPUT:
-------------------
starting up on localhost port 20000

waiting for a connection

connection from: ('127.0.0.1', 21570)

Waiting for data from the client

size of the mft file is going to be sent

file size: 102400

MFT (compressed) extracted succesfuly to: C:\temp\extractedMFT\127.0.0.1_mft_compressed

MFT decompressed succesfuly and saved to: C:\temp\extractedMFT\127.0.0.1_mft_decompressed

MFT analyzed succesfuly and results saved to log file: C:\temp\logfile.txt 

no more data from: ('127.0.0.1', 21570)

waiting for a connection
