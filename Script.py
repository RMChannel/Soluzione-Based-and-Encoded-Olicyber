from pwn import *
from ast import literal_eval
import base64
r=remote("based.challs.olicyber.it", 10600)
datab=str(r.recvuntil(b"Ora dammi una risposta"))
while True:
    i1=datab.rfind('{')
    i2=datab.rfind("}")+1
    datar=literal_eval(datab[i1:i2])["message"]
    if "Converti questo a esadecimale" in datab:    result=datar.encode().hex()
    elif "Converti questo da esadecimale" in datab: result=bytes.fromhex(datar).decode()
    elif "Converti questo a base64" in datab:   result=base64.b64encode(bytes(datar,'utf-8')).decode('utf-8')
    elif "Converti questo da base64" in datab:  result=base64.b64decode(bytes(datar,'utf-8')).decode('utf-8')
    elif "Converti questo da binario" in datab:
        while (len(datar)%8)!=0:
            datar="0"+datar
        list=[]
        temp=""
        i2=0
        for i in datar:
            if (i2<8):
                temp=temp+i
                i2+=1
            else:
                list.append(temp)
                temp=i
                i2=1
        list.append(temp)
        result=""
        for i in list:
            result=result+(chr(int(i,2)))
    elif "Converti questo a binario" in datab:  result=(''.join(format(ord(i), '08b') for i in datar)).replace(" ","")[1:]
    answer=('{"answer":"'+str(result)+'"}').encode()
    r.sendline(answer)
    datab=str(r.recvlines(6))
    if "flag" in datab:
        print(datab)
        exit()