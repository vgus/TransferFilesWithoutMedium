import base64

with open('test.txt','rb') as codificado, open("Nuevo2.pdf", "wb") as pdf_file:
    decoded_string = base64.b64decode(codificado.read())
    #print(encoded_string)
    pdf_file.write(decoded_string)