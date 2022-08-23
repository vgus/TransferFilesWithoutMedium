# TransferFilesWithoutMedium

When you have access to a file in a computer but you can't download to a medium (USB, CD, etc)  and even upload to the cloud.

I was in the situtation where I need I need files from a computer (I have to declare that these files are mine like paycheck receipt), but I can't connect a USB or even upload to the cloud because these services are restricted. 

Using this program you make a series of QRs to transfer a file using any QR cellphone app and recontruct the file in another machine.

## Requirements

This program use python3 and the following modules: 

- Pillow = 8.3.2
- qrcode = 7.3

To install these modules:

```
pip install --upgrade qrcode pillow google-api-python-client google-auth-httplib2 google-auth-oauthlib

```

## Use

You have to:
1. Type or copy the content of the encode.py in origin computer that have the file.
2. Change the variable destination with your email.
3. Make a directory under in the same directory where the encode.py is located and named "QrsIms"
4. run the file using the name of the file that you want to sent.

>python3 encode.py example.pdf

5. It makes a series of a QRs in the directory QrsIms
6. You have to scan that series of QRs, they are prepared to make a email.
7. With all the information you already have, you have to make a file txt (e.g. file.txt) in the destination computer
8. You have to run in the destination computer the file Decode.py adding the name of the file you just created and the name of the file that is in the subject of the emails.

>python3 encode.py file.txt file.pdf

9. Test the file. 
   - If you can open the file, redo the process from point 4.

# Disclaimer

Make sure that you have the property and the right of the files you are transfering.

