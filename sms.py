from telethon.sync import TelegramClient
from telethon.tl.types import InputPeerUser
from telethon.errors.rpcerrorlist import PeerFloodError
import configparser
import os, sys
import csv
import random
import time

red="\033[1;31m"
green="\033[1;32m"
cyan="\033[1;36m"
SLEEP_TIME = 30

class main():

    def banner():
        
        print(f"""
    {green}╔═╗ ┌─┐ ┬─┐ ┌─┐ ┌─┐ ┌─┐ ┌─┐ ┬─┐
    {green}╚═╗ │   ├┬┘ ├─┤ ├─┘ ├─┘ ├┤  ├┬┘
    {green}╚═╝ └─┘ ┴└─ ┴ ┴ ┴   ┴   └─┘ ┴└─

                versão: 1.0.0
            https://t.me/oDeskrin
            """)

    def send_sms():
        try:
            cpass = configparser.RawConfigParser()
            cpass.read('config.data')
            api_id = cpass['cred']['id']
            api_hash = cpass['cred']['hash']
            phone = cpass['cred']['phone']
        except KeyError:
            os.system('clear')
            main.banner()
            print(red+"[!] Execute: python3 setup.py antes.\n")
            sys.exit(1)

        client = TelegramClient(phone, api_id, api_hash)
         
        client.connect()
        if not client.is_user_authorized():
            client.send_code_request(phone)
            os.system('clear')
            main.banner()
            client.sign_in(phone, input(green+'[+] Insira o código recebido: '+red))
        
        os.system('clear')
        main.banner()
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
        print(green+"[1] Enviar SMS por ID de usuário\n[2] Enviar SMS por NOME de usuário")
        mode = int(input(green+"[+] Escolha: "+red))
         
        message = input(green+"[+] Insira uma mensagem: "+red)
         
        for user in users:
            if mode == 2:
                if user['username'] == "":
                    continue
                receiver = client.get_input_entity(user['username'])
            elif mode == 1:
                receiver = InputPeerUser(user['id'],user['access_hash'])
            else:
                print(red+"[!] Modo inválido, saindo!")
                client.disconnect()
                sys.exit()
            try:
                print(green+"[+] Enviando mensagem para:", user['name'])
                client.send_message(receiver, message.format(user['name']))
                print(green+"[+] Esperando {} segundos".format(SLEEP_TIME))
                time.sleep(SLEEP_TIME)
            except PeerFloodError:
                print(red+"[!] Erro de flod do telegram. \n[!] Script parando. \n[!] Tente novamente mais tarde.")
                client.disconnect()
                sys.exit()
            except Exception as e:
                print(red+"[!] Erro:", e)
                print(red+"[!] Tentando continuar...")
                continue
        client.disconnect()
        print(green+"[!] Mensagem enviada a todos os usuários.")

main.send_sms()
