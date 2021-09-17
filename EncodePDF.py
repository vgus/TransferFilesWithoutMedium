import base64
from sys import argv
import qrcode

file = argv[1]
chunk = 2200
destination = 'mail@example.com'

with open(file, "rb") as pdf_file, open('archivoab64.txt','wb') as codificado:
    encoded_string = base64.b64encode(pdf_file.read())
    codificado.write(encoded_string)

toQr = encoded_string.decode('UTF-8')

chunkInit = 0
for i,chunkNum in enumerate(range(chunk,len(toQr)+chunk-1,chunk)):
    mail = f'mailto:{destination}?subject={file}&body={i}\n'  
    img = qrcode.make(mail+toQr[chunkInit:chunkNum])
    chunkInit = chunkNum
    nameEx = f'QrsIms/{file}{i}.png'
    f = open(nameEx, "wb")
    img.save(f)
    f.close()
    

