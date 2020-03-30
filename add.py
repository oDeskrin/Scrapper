#!/bin/env python3
from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty, InputPeerChannel, InputPeerUser
from telethon.errors.rpcerrorlist import PeerFloodError, UserPrivacyRestrictedError
from telethon.tl.functions.channels import InviteToChannelRequest
import configparser
import os, sys
import csv
import traceback
import time
import random

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
input_file = sys.argv[1]
users = []
with open(input_file, encoding='UTF-8') as f:
    rows = csv.reader(f,delimiter=",",lineterminator="\n")
    next(rows, None)
    for row in rows:
        user = {}
        user['username'] = row[0]
        user['id'] = int(row[1])
        user['access_hash'] = int(row[2])
        user['name'] = row[3]
        users.append(user)
 
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
 
i=0
for group in groups:
    print(green+'['+cyan+str(i)+green+']'+cyan+' - '+group.title)
    i+=1

print(green+'[+] Selecione um grupo para adicionar os usuários')
g_index = input(green+"[!] Escolha o número referente ao grupo: "+red)
target_group=groups[int(g_index)]
 
target_group_entity = InputPeerChannel(target_group.id,target_group.access_hash)
 
print(green+"1] Adicionar por ID de usuário\n[2] Adicionar por NOME de usuário")
mode = int(input(green+"[+] Opção: "+red)) 
n = 0
 
for user in users:
    n += 1
    if n % 50 == 0:
	    time.sleep(1)
	    try:
	        print ("[+] Adicionando {}".format(user['id']))
	        if mode == 1:
	            if user['username'] == "":
	                continue
	            user_to_add = client.get_input_entity(user['username'])
	        elif mode == 2:
	            user_to_add = InputPeerUser(user['id'], user['access_hash'])
	        else:
	            sys.exit(red+"[!] Modo selecionado inválido. Tente novamente.")
	        client(InviteToChannelRequest(target_group_entity,[user_to_add]))
	        print(green+"[+] O intervá-lo de adição e de 1/15 segundos")
	        time.sleep(random.randrange(1, 15))
	    except PeerFloodError:
	        print(red+"[!] Erro de flod do telegram. \n[!] Script parando. \n[!] Tente novamente mais tarde.")
	    except UserPrivacyRestrictedError:
	        print(red+"[!] Este usuário não permite que o adicione, pulando.")
	    except:
	        traceback.print_exc()
	        print(red+"[!] Erro inesperado.")
	        continue
