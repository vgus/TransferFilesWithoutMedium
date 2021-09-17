import base64
from sys import argv

file = argv[1]
fileDest = argv[2]

with open(file,'rb') as codificado, open(fileDest, "wb") as pdf_file:
    decoded_string = base64.b64decode(codificado.read())
    #print(encoded_string)
    pdf_file.write(decoded_string)