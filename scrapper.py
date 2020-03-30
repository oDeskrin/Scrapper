from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty
import os, sys
import configparser
import csv
import time

red="\033[1;31m"
green="\033[1;32m"
cyan="\033[1;36m"

def banner():
    print(f"""
    {green}╔═╗ ┌─┐ ┬─┐ ┌─┐ ┌─┐ ┌─┐ ┌─┐ ┬─┐
    {green}╚═╗ │   ├┬┘ ├─┤ ├─┘ ├─┘ ├┤  ├┬┘
    {green}╚═╝ └─┘ ┴└─ ┴ ┴ ┴   ┴   └─┘ ┴└─

                versão: 1.0.0
            https://t.me/oDeskrin
            """)

cpass = configparser.RawConfigParser()
cpass.read('config.data')

try:
    api_id = cpass['cre']['id']
    api_hash = cpass['cre']['hash']
    phone = cpass['cre']['phone']
    client = TelegramClient(phone, api_id, api_hash)
except KeyError:
    os.system('clear')
    banner()
    print(red+"[!] Execute: python3 setup.py antes.\n")
    sys.exit(1)

client.connect()
if not client.is_user_authorized():
    client.send_code_request(phone)
    os.system('clear')
    banner()
    client.sign_in(phone, input(green+'[+] Insira o código recebido: '+red))
 
os.system('clear')
banner()
chats = []
last_date = None
chunk_size = 200
groups=[]
 
result = client(GetDialogsRequest(
             offset_date=last_date,
             offset_id=0,
             offset_peer=InputPeerEmpty(),
             limit=chunk_size,
             hash = 0
         ))
chats.extend(result.chats)
 
for chat in chats:
    try:
        if chat.megagroup== True:
            groups.append(chat)
    except:
        continue
 
print(green+'[+] Selecione um grupo para extrair usuários:'+red)
i=0
for g in groups:
    print(green+'['+cyan+str(i)+green+']'+cyan+' - '+ g.title)
    i+=1
 
print('')
g_index = input(green+"[+] Escolha o número referente ao grupo: "+red)
target_group=groups[int(g_index)]
 
print(green+'[+] Buscando usuários...')
time.sleep(1)
all_participants = []
all_participants = client.get_participants(target_group, aggressive=True)
 
print(green+'[+] Salvando no arquivo...')
time.sleep(1)
with open("membros.csv","w",encoding='UTF-8') as f:
    writer = csv.writer(f,delimiter=",",lineterminator="\n")
    writer.writerow(['username','user id', 'access hash','name','group', 'group id'])
    for user in all_participants:
        if user.username:
            username= user.username
        else:
            username= ""
        if user.first_name:
            first_name= user.first_name
        else:
            first_name= ""
        if user.last_name:
            last_name= user.last_name
        else:
            last_name= ""
        name= (first_name + ' ' + last_name).strip()
        writer.writerow([username,user.id,user.access_hash,name,target_group.title, target_group.id])      
print(green+'[+] Membros extraidos com sucesso.')
