# TEXT파일에 있는 웹사이트들를 읽고 QR코드를 생성하기 
import qrcode
# with open('C:\\Users\\user\\Documents\\MS AI SCHOOL\\DAY8_Python\\site_list.txt','rt', encoding= 'UTF8') as f:
with open(r'C:\Users\user\Documents\MS AI SCHOOL\DAY8_Python\site_list.txt','rt', encoding= 'UTF8') as f:
    read_lines = f.readlines()

    for line in read_lines:
        line = line.strip()
        print(line)

        qr_data = line
        qr_image = qrcode.make(qr_data)
    
        qr_image.save('C:\\Users\\user\\Documents\\MS AI SCHOOL\\DAY8_Python\\' + qr_data+'.png')